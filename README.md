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
