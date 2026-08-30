
-- DIM_CUSTOMER (Hybrid SCD)
-- Type 2 (versioned): address, city, state, country
-- Type 1 (overwrite):  first_name, last_name, email, phone,
--                       gender, role, company_department
-- Stored raw, not derived: birth_date (compute age at query time)

CREATE TABLE dim_customer (
    customer_key        SERIAL PRIMARY KEY,      -- surrogate key, unique per VERSION
    user_id              INT NOT NULL,            -- natural key, same across all versions

    -- Type 1 attributes (overwritten in place, no history)
    first_name           VARCHAR(100),
    last_name             VARCHAR(100),
    email                 VARCHAR(200),
    phone                 VARCHAR(50),
    gender                VARCHAR(20),
    role                  VARCHAR(50),
    company_department    VARCHAR(100),
    birth_date            DATE,                   -- store raw fact, compute age when needed

    -- Type 2 attributes (versioned — new row on change)
    address               VARCHAR(300),
    city                  VARCHAR(100),
    state                 VARCHAR(100),
    country               VARCHAR(100),

    -- SCD2 metadata
    effective_date        DATE NOT NULL,
    end_date               DATE,                  -- NULL = currently active
    is_current             BOOLEAN NOT NULL DEFAULT TRUE
);

-- Fast lookup of the current version of any customer
CREATE INDEX idx_dim_customer_current
    ON dim_customer (user_id, is_current);



-- INITIAL LOAD — first version of every customer

INSERT INTO dim_customer (
    user_id, first_name, last_name, email, phone, gender, role,
    company_department, birth_date, address, city, state, country,
    effective_date, end_date, is_current
)
SELECT
    user_id, first_name, last_name, email, phone, gender, role,
    company_department, birth_date, address, city, state, country,
    CURRENT_DATE AS effective_date,
    NULL AS end_date,
    TRUE AS is_current
FROM users;



-- SCD2 UPDATE LOGIC — run this when source `users` data changes
-- Example: user_id 5 moves from Phoenix to Seattle


-- Step 1: Close out the OLD row (metadata only — never touch location columns)
UPDATE dim_customer
SET end_date = CURRENT_DATE - INTERVAL '1 day',
    is_current = FALSE
WHERE user_id = 5
  AND is_current = TRUE;

-- Step 2: Insert the NEW row with the updated location
INSERT INTO dim_customer (
    user_id, first_name, last_name, email, phone, gender, role,
    company_department, birth_date, address, city, state, country,
    effective_date, end_date, is_current
)
VALUES (
    5, 'Emily', 'Johnson', 'emily.johnson@x.dummyjson.com', '+81 965-431-30...',
    'female', 'admin', 'Research and Development', '1996-05-30',
    '1234 New Street', 'Seattle', 'WA', 'United States',
    CURRENT_DATE, NULL, TRUE
);



-- SANITY CHECKS

-- Every user_id should have exactly ONE row where is_current = TRUE
SELECT user_id, COUNT(*)
FROM dim_customer
WHERE is_current = TRUE
GROUP BY user_id
HAVING COUNT(*) != 1;
-- should return ZERO rows — if it returns any, something is wrong

-- See full version history for a specific customer
SELECT customer_key, user_id, city, state, effective_date, end_date, is_current
FROM dim_customer
WHERE user_id = 5
ORDER BY effective_date;
