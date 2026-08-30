
-- FACT_ORDER_ITEMS
-- Grain: one row per product per order

CREATE TABLE fact_order_items (
    order_item_key    SERIAL PRIMARY KEY,
    cart_id            INT NOT NULL,           -- degenerate dimension
    date_key            INT REFERENCES dim_date(date_key),
    customer_key        INT REFERENCES dim_customer(customer_key),
    product_key          INT REFERENCES dim_product(product_key),

    quantity              INT NOT NULL,
    price                  NUMERIC(10,2) NOT NULL,     -- price paid at time of purchase
    discount_percentage     NUMERIC(5,2),
    total                     NUMERIC(10,2),
    discounted_total           NUMERIC(10,2)
);



-- LOAD: join order_items -> orders -> dimensions

INSERT INTO fact_order_items (
    cart_id, date_key, customer_key, product_key,
    quantity, price, discount_percentage, total, discounted_total
)
SELECT
    oi.cart_id,
    TO_CHAR(o.order_date, 'YYYYMMDD')::INT AS date_key,
    dc.customer_key,
    dp.product_key,
    oi.quantity,
    oi.price,
    oi.discount_percentage,
    oi.total,
    oi.discounted_total
FROM order_items oi
JOIN orders o
    ON oi.cart_id = o.cart_id
JOIN dim_product dp
    ON oi.product_id = dp.product_id
JOIN dim_customer dc
    ON o.user_id = dc.user_id
   AND o.order_date >= dc.effective_date
   AND (o.order_date < dc.end_date OR dc.end_date IS NULL);



-- SANITY CHECKS

-- 1. Row count should match order_items exactly (one-to-one on grain)
SELECT
    (SELECT COUNT(*) FROM order_items) AS source_count,
    (SELECT COUNT(*) FROM fact_order_items) AS fact_count;
-- these two numbers MUST match — if fact_count is higher, a join is fanning out
-- (usually means the dim_customer date-range join has overlapping/bad ranges)
-- if fact_count is lower, some rows failed to join (usually a missing dim row)

-- 2. Validate against orders' pre-aggregated totals (the check we planned earlier)
SELECT
    f.cart_id,
    SUM(f.discounted_total) AS fact_total,
    o.discounted_total AS orders_table_total
FROM fact_order_items f
JOIN orders o ON f.cart_id = o.cart_id
GROUP BY f.cart_id, o.discounted_total
HAVING SUM(f.discounted_total) != o.discounted_total;
-- should return ZERO rows — any row returned here is a real data integrity bug



-- EXAMPLE ANALYTICAL QUERY — the whole point of the model
-- Revenue by state, using the CORRECT historical customer state

SELECT
    dc.state,
    dd.year,
    dd.month_name,
    SUM(f.discounted_total) AS revenue
FROM fact_order_items f
JOIN dim_customer dc ON f.customer_key = dc.customer_key
JOIN dim_date dd ON f.date_key = dd.date_key
GROUP BY dc.state, dd.year, dd.month_name
ORDER BY dd.year, dd.month_name;
