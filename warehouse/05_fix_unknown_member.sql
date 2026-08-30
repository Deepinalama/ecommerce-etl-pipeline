
-- FIX: Kimball "unknown member" pattern for dim_product
-- Handles order_items rows whose product_id has no match in
-- the products table (94 such rows in this dataset).

-- Insert a placeholder row with a reserved surrogate key.
-- Using -1 explicitly (instead of letting SERIAL assign it) so it's
-- always identifiable and never collides with a real product_key.
INSERT INTO dim_product (
    product_key, product_id, title, category, brand, stock,
    dimensions_height, dimensions_width, dimensions_depth
)
OVERRIDING SYSTEM VALUE
VALUES (
    -1, -1, 'Unknown Product', 'Unknown', 'Unknown', NULL,
    NULL, NULL, NULL
);

-- Rebuild fact_order_items using LEFT JOIN + COALESCE
-- so unmatched product_ids map to the placeholder instead of
-- being dropped from the fact table entirely.
TRUNCATE fact_order_items;

INSERT INTO fact_order_items (
    cart_id, date_key, customer_key, product_key,
    quantity, price, discount_percentage, total, discounted_total
)
SELECT
    oi.cart_id,
    TO_CHAR(o.order_date, 'YYYYMMDD')::INT AS date_key,
    dc.customer_key,
    COALESCE(dp.product_key, -1) AS product_key,
    oi.quantity,
    oi.price,
    oi.discount_percentage,
    oi.total,
    oi.discounted_total
FROM order_items oi
JOIN orders o
    ON oi.cart_id = o.cart_id
LEFT JOIN dim_product dp
    ON oi.product_id = dp.product_id
JOIN dim_customer dc
    ON o.user_id = dc.user_id
   AND o.order_date >= dc.effective_date
   AND (o.order_date < dc.end_date OR dc.end_date IS NULL);

-- Verify — should now equal order_items count (114)
SELECT COUNT(*) FROM fact_order_items;

-- See how much revenue is attached to unknown products
-- (a genuinely useful data-quality metric for your README)
SELECT
    SUM(discounted_total) AS revenue_from_unmatched_products,
    COUNT(*) AS line_items_affected
FROM fact_order_items
WHERE product_key = -1;
