
-- DIM_PRODUCT (SCD Type 1 — overwrite on change, no history)
-- One row per product. Surrogate key is independent of source system.

CREATE TABLE dim_product (
    product_key         SERIAL PRIMARY KEY,      -- surrogate key (warehouse-generated)
    product_id          INT NOT NULL UNIQUE,      -- natural key from source `products` table
    title                VARCHAR(200),
    category             VARCHAR(100),
    brand                VARCHAR(100),
    stock                INT,                     -- current stock level 
    dimensions_height    DOUBLE PRECISION,
    dimensions_width     DOUBLE PRECISION,
    dimensions_depth     DOUBLE PRECISION
);


-- LOAD LOGIC (Type 1 — simple upsert, no history tracking)

INSERT INTO dim_product (
    product_id, title, category, brand, stock,
    dimensions_height, dimensions_width, dimensions_depth
)
SELECT
    product_id, title, category, brand, stock,
    dimensions_height, dimensions_width, dimensions_depth
FROM products
ON CONFLICT (product_id)
DO UPDATE SET
    title              = EXCLUDED.title,
    category           = EXCLUDED.category,
    brand              = EXCLUDED.brand,
    stock              = EXCLUDED.stock,
    dimensions_height  = EXCLUDED.dimensions_height,
    dimensions_width   = EXCLUDED.dimensions_width,
    dimensions_depth   = EXCLUDED.dimensions_depth;

-- check
SELECT COUNT(*) FROM dim_product;
SELECT * FROM dim_product LIMIT 5;
