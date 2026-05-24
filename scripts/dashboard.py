import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus



password = quote_plus("Ichig0kur0s@ki")

engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/ecommerce"
)



st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

st.title("E-Commerce Analytics Dashboard")



@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)



# Total Revenue
revenue_query = """
SELECT SUM(quantity * price) AS total_revenue
FROM order_items;
"""

# Total Orders
orders_query = """
SELECT COUNT(*) AS total_orders
FROM orders;
"""

# Total Customers
customers_query = """
SELECT COUNT(*) AS total_customers
FROM users;
"""

# Top Products
top_products_query = """
SELECT 
    p.title,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p 
    ON oi.product_id = p.product_id
GROUP BY p.title
ORDER BY total_sold DESC
LIMIT 10;
"""

# Revenue Trend
revenue_trend_query = """
SELECT 
    o.cart_id,
    SUM(oi.total) AS revenue
FROM orders o
JOIN order_items oi 
    ON o.cart_id = oi.cart_id
GROUP BY o.cart_id
ORDER BY o.cart_id;
"""
total_revenue = load_data(revenue_query).iloc[0, 0]
total_orders = load_data(orders_query).iloc[0, 0]
total_customers = load_data(customers_query).iloc[0, 0]

top_products = load_data(top_products_query)



st.subheader(" Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(" Revenue", f"${total_revenue:,.2f}")
col2.metric(" Orders", total_orders)
col3.metric(" Customers", total_customers)



st.subheader("Top Selling Products")

st.bar_chart(
    top_products.set_index("title")
)



st.subheader(" Revenue Trend")

try:
    trend = load_data(revenue_trend_query)

    st.line_chart(trend.set_index("cart_id"))


    

except Exception as e:
    st.error(f"Error loading revenue trend: {e}")