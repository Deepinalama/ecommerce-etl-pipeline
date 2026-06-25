import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "db_name")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "db_password")

encoded_password = quote_plus(DB_PASSWORD)

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:5432/{DB_NAME}"
)

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("E-Commerce Analytics Dashboard")

@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

revenue_query = "SELECT SUM(quantity * price) AS total_revenue FROM order_items;"
orders_query = "SELECT COUNT(*) AS total_orders FROM orders;"
customers_query = "SELECT COUNT(*) AS total_customers FROM users;"

top_products_query = """
SELECT p.title, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.title
ORDER BY total_sold DESC
LIMIT 10;
"""

revenue_trend_query = """
SELECT o.cart_id, SUM(oi.total) AS revenue
FROM orders o
JOIN order_items oi ON o.cart_id = oi.cart_id
GROUP BY o.cart_id
ORDER BY o.cart_id;
"""

try:
    total_revenue = load_data(revenue_query).iloc[0, 0] or 0.0
    total_orders = load_data(orders_query).iloc[0, 0] or 0
    total_customers = load_data(customers_query).iloc[0, 0] or 0
    top_products = load_data(top_products_query)
    revenue_trend = load_data(revenue_trend_query)  
except Exception as e:
    st.warning(f"Database error: {e}. Please run your data pipeline first.")
    total_revenue, total_orders, total_customers = 0.0, 0, 0
    top_products = pd.DataFrame(columns=["title", "total_sold"])
    revenue_trend = pd.DataFrame(columns=["cart_id", "revenue"])

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"${total_revenue:,.2f}")
col2.metric("Orders", total_orders)
col3.metric("Customers", total_customers)


st.subheader("Top Selling Products")
if not top_products.empty:
    st.bar_chart(top_products.set_index("title"))
else:
    st.info("No product data available.")


st.subheader("Revenue Trend")
if not revenue_trend.empty:
    st.line_chart(revenue_trend.set_index("cart_id"))  
    st.info("No revenue trend data available.")