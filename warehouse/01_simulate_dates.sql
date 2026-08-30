
--Add order_date to orders table

ALTER TABLE orders ADD COLUMN order_date DATE;


--  Simulate realistic order dates


WITH bounds AS (
    SELECT MIN(cart_id) AS min_id, MAX(cart_id) AS max_id
    FROM orders
),
scored AS (
    SELECT
        o.cart_id,
        -- normalize cart_id to a 0-1 position (0 = earliest, 1 = most recent)
        (o.cart_id - b.min_id)::FLOAT / NULLIF(b.max_id - b.min_id, 0) AS position,
        b.min_id,
        b.max_id
    FROM orders o, bounds b
)
UPDATE orders o
SET order_date = (
    -- base date: 180 days ago + (position * 180 days) skews later carts to recent dates
    CURRENT_DATE - INTERVAL '180 days'
    + (s.position * 180 || ' days')::INTERVAL
    -- random jitter of +/- 10 days so it's not a perfectly straight line
    + ((RANDOM() * 20 - 10) || ' days')::INTERVAL
)::DATE
FROM scored s
WHERE o.cart_id = s.cart_id;

-- Sanity check
SELECT MIN(order_date), MAX(order_date), COUNT(*) FROM orders;



-- STEP 3: Build dim_date (calendar table)

CREATE TABLE dim_date (
    date_key        INT PRIMARY KEY,        -- YYYYMMDD
    full_date       DATE NOT NULL,
    day_of_week     VARCHAR(10),
    day_of_month    INT,
    month           INT,
    month_name      VARCHAR(10),
    quarter         INT,
    year            INT,
    is_weekend      BOOLEAN
);

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT AS date_key,
    d AS full_date,
    TO_CHAR(d, 'Day') AS day_of_week,
    EXTRACT(DAY FROM d)::INT AS day_of_month,
    EXTRACT(MONTH FROM d)::INT AS month,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(QUARTER FROM d)::INT AS quarter,
    EXTRACT(YEAR FROM d)::INT AS year,
    EXTRACT(ISODOW FROM d) IN (6, 7) AS is_weekend
FROM generate_series(
    (SELECT MIN(order_date) FROM orders) - INTERVAL '7 days',
    (SELECT MAX(order_date) FROM orders) + INTERVAL '7 days',
    INTERVAL '1 day'
) AS d;

--check
SELECT COUNT(*) FROM dim_date;
SELECT * FROM dim_date ORDER BY full_date LIMIT 5;
