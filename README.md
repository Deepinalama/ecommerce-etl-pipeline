 E-Commerce ETL Pipeline

An end-to-end **ETL (Extract, Transform, Load)** pipeline that extracts nested e-commerce JSON data, transforms and normalizes it into relational tables, and loads it into **PostgreSQL** for analytics — with an interactive **Streamlit** dashboard for visualization.

> 🔗 Part of a data engineering project series — this pipeline feeds data into the [NLQ SQL Chatbot](https://github.com/Deepinalama/nlq-sql-chatbot) for AI-powered natural language querying.

---

 Features

-  **Extract** — Pulls nested JSON e-commerce data from API/files
-  **Transform** — Cleans, normalizes, and structures data using Pandas
-  **Load** — Loads processed data into PostgreSQL relational tables
-  **Dashboard** — Interactive Streamlit UI for sales and analytics visualization
-  **Dockerized** — Fully containerized with Docker Compose

---

## Data Warehouse Layer

Building on the existing ETL pipeline, this project also includes a **Kimball-style star schema** layered on top of the OLTP order data — turning raw transactional tables into a model built for analytics.

![Star Schema ERD](docs/star_schema_erd.png)

**What's in it:**
- `dim_date` — calendar dimension (order dates simulated where the source lacked timestamps; see design notes)
- `dim_product` — Type 1 SCD (catalog attributes, overwritten on change)
- `dim_customer` — hybrid SCD: Type 2 on location (address/city/state/country), Type 1 on everything else — tracks *where a customer was* at the time of each historical order, not just where they are now
- `fact_order_items` — transaction fact table, grain of one row per product per order, validated to reconcile exactly against source data

**Why this matters:** the raw OLTP schema is optimized for transactions, not analysis. This layer makes questions like *"revenue by state, using the customer's location at the time of the order"* — not their current location — actually answerable, correctly, even after a customer moves.

Full design reasoning, including two real data-integrity bugs found and fixed during validation (an SCD2 effective-date bug and an incomplete source catalog handled via Kimball's unknown-member pattern), is documented in [`warehouse/DESIGN_NOTES.md`](warehouse/DESIGN_NOTES.md).

**Example output:**

![Revenue by state demo](docs/revenue_by_state_demo.png)

**To run it**, execute the SQL files in `warehouse/` in numbered order (`01` through `05`) against the Postgres database populated by the existing ETL pipeline.
 Tech Stack

| Layer | Technology |
|---|---|
| **Data Processing** | Python, Pandas |
| **Database** | PostgreSQL |
| **ORM/Connector** | SQLAlchemy, psycopg2 |
| **Dashboard** | Streamlit |
| **Containerization** | Docker Compose |

---

Project Structure

```
ecommerce-etl-pipeline/
├── data/
│   └── raw/                  # Raw JSON source data
├── scripts/
│   ├── extract.py            # Data extraction logic
│   ├── transform.py          # Data cleaning and normalization
│   ├── load.py               # PostgreSQL loading logic
│   └── dashboard.py          # Streamlit dashboard
├── docker-compose.yml        # Postgres + Streamlit services
├── dockerfile                # App container definition
├── requirements.txt          # Python dependencies
└── .gitignore
```

---

 ETL Flow

```
Raw JSON Data (nested e-commerce records)
        ↓  EXTRACT
Parse JSON, flatten nested structures
        ↓  TRANSFORM
Clean nulls, normalize into relational tables
(customers, orders, products, order_items)
        ↓  LOAD
Insert into PostgreSQL via SQLAlchemy
        ↓
Streamlit Dashboard for analytics
```

---

 Database Schema

| Table | Description |
|---|---|
| `customers` | Customer profiles and contact info |
| `orders` | Order headers with status and dates |
| `products` | Product catalog with pricing |
| `order_items` | Line items linking orders to products |

---

 Getting Started

 Prerequisites
- Docker Desktop

 1. Clone the repo
```bash
git clone https://github.com/Deepinalama/ecommerce-etl-pipeline.git
cd ecommerce-etl-pipeline
```

 2. Set up environment variables
Create a `.env` file:
```
DB_HOST=db
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your_password
```

3. Start services
```bash
docker-compose up -d --build
```

 4. Run the ETL pipeline
```bash
docker exec -it ecommerce_dashboard python scripts/extract.py
docker exec -it ecommerce_dashboard python scripts/transform.py
docker exec -it ecommerce_dashboard python scripts/load.py
```

 5. View the dashboard
Open `http://localhost:8501` in your browser

---

 Dashboard Features

- Sales revenue trends over time
- Top customers by order value
- Product performance analysis
- Order status breakdown

---

 Related Projects

| Project | Description |
|---|---|
| **E-Commerce ETL Pipeline** | This project — data ingestion and transformation |
| [NLQ SQL Chatbot](https://github.com/Deepinalama/nlq-sql-chatbot) | AI-powered natural language querying on top of this data |
| [ML Platform](https://github.com/Deepinalama/ml-platform) | Full ML platform with Airflow, FastAPI, Django REST + JWT |
