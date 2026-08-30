# Orders Star Schema — Design Notes

## Business process & grain
Models the order-placement process. Grain: **one row per product per order**
(matches the source `order_items` table). Rejected order-level grain because it
would lose product-level detail needed for category/product analytics.

## Fact table
`fact_order_items` — transaction fact table. Facts: `quantity`, `price`,
`discount_percentage`, `total`, `discounted_total`. `cart_id` kept as a
degenerate dimension (no separate `dim_order` needed — it has no descriptive
attributes of its own).

## Dimensions

**dim_date** — standard calendar dimension. The source data had no order
timestamp at all, so `order_date` was simulated (weighted toward recent dates
via cart_id position + jitter, not uniform random, to avoid an obviously
artificial flat distribution). In production this would come from the source
system's `created_at` or from ingestion/CDC event metadata — flagged here so
it's clear this is a workaround, not the intended design.

**dim_product** — SCD Type 1 (overwrite, no history). Justification: the fact
table already snapshots `price` at time of purchase (`order_items.price`), so
even if a product's catalog attributes change later, historical order data
stays correct. There's nothing that specifically requires knowing what a
product's category/brand was on a past date.

**dim_customer** — hybrid SCD. `address`/`city`/`state`/`country` are Type 2
(versioned) because "which region did this order's revenue come from at the
time" is a real historical question — this is the textbook SCD2 case.
Everything else (`name`, `email`, `phone`, `role`, `department`) is Type 1,
since there's no analytical need to know their historical values.
`birth_date` is stored raw rather than a derived `age` column, since age
changes continuously and would go stale — it's computed at query time instead.

Excluded entirely: bank card/IBAN, IP, MAC address, user agent, physical
attributes (height/weight/blood group/eye color). These are synthetic dataset
noise, and in a real system, several (card numbers, IBAN) would be a genuine
data governance/PCI concern to bring into an analytics warehouse at all.

## Key design pattern: dimension versioning via date-range join
Fact rows link to the dimension version that was valid **at the time of the
order**, not the current version:

```sql
JOIN dim_customer dc
    ON orders.user_id = dc.user_id
   AND orders.order_date >= dc.effective_date
   AND (orders.order_date < dc.end_date OR dc.end_date IS NULL)
```

This is what makes SCD2 actually work — a March order from a customer who
later moved still correctly attributes to their March address.

## Validation
- Row count of `fact_order_items` matches `order_items` exactly (114/114,
  grain preserved, no join fan-out).
- `SUM(discounted_total)` per `cart_id` in the fact table reconciles exactly
  against the pre-aggregated total stored in the source `orders` table.
- Every `user_id` has exactly one `is_current = TRUE` row in `dim_customer`
  at any time.

## Debugging log

**Issue 1 — SCD2 initial load used the wrong `effective_date`.**
The initial `dim_customer` load set `effective_date = CURRENT_DATE` for every
customer's first version. Since simulated `order_date` values span the past
180 days, the date-range join (`order_date >= effective_date`) rejected
almost every order — only 1 of 114 fact rows loaded. Caught by the
`source_count = fact_count` sanity check. Fix: backdated the initial
`effective_date` (e.g. `2000-01-01`) so it covers the full order history —
the correct convention for a bulk historical load, since "today" is when the
data was *loaded*, not when the customer record became *true*.

**Issue 2 — `products` table was incomplete relative to `order_items`.**
After fixing Issue 1, row count was still 20/114. Root cause: `products` has
only 30 rows, but `order_items` references product IDs the source dataset
never fully populated into `products` (94 orphaned references, confirmed via
`LEFT JOIN ... WHERE product.id IS NULL`). Rather than silently dropping
those 94 rows (~$643K in revenue), applied Kimball's **unknown-member
pattern**: a placeholder `dim_product` row (`product_key = -1`), with the
fact load switched to `LEFT JOIN` + `COALESCE`. This keeps referential
integrity in the fact table while making the data-quality gap visible and
queryable (`WHERE product_key = -1`) instead of invisible.
