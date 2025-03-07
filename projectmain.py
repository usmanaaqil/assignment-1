import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# Define TiDB Connection (Replace with actual credentials)
connection_string = ("mysql+pymysql://2MEsqjfqfNMNnUw.root:T75oLIvaZ0b2UeN1@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/usman?ssl_ca=C:/Users/Admin/Downloads/isrgrootx1 (3).pem")
engine = create_engine(connection_string)

# Fetch all orders and products data with distinct column names
query_all_data = """
    SELECT 
        o.order_id AS order_id_orders,
        o.order_date,
        o.ship_mode,
        o.segment,
        o.country,
        o.city,
        o.state,
        o.postal_code,
        o.region,
        p.order_id AS order_id_products,
        p.product_id,
        p.category,
        p.sub_category,
        p.cost_price,
        p.list_price,
        p.quantity,
        p.discount_percent,
        p.discount,
        p.sale_price,
        p.profit
    FROM orders_table o  
    JOIN products_table p ON o.order_id = p.order_id;
"""
df_all = pd.read_sql(query_all_data, engine)

# Streamlit App
st.title("Retail Order Data Analysis")

# First sidebar selectbox
option1 = st.sidebar.selectbox(
    "Select Analysis", 
    [
        "Top 10 Revenue Products",
        "Top 5 Cities with Highest Profit",
        "Total Discount per Category",
        "Average sale price per product Category",
        "Average sale price by highest region",
        "Total profit per category",
        "Top 3 segments highest quantity of orders",
        "Determine the avg discount percentage given per region",
        "Product category with the highest total profit",
        "Total revenue generated per year"
    ], 
    index=0  
)

# Second sidebar selectbox
option2 = st.sidebar.selectbox(
    "Select Analysis for me", 
    [
        "Total number of unique products sold per region",
        "Top 5 states with total discount",
        "Total profit for each sub category",
        "Average sale price per product per city",
        "Determine the region with the highest total number of orders",
        "Top 3 categories that contributed to the highest total revenue",
        "Top 5 customers city wise with the highest order count",
        "Percentage of orders that used each ship mode",
        "Total revenue per segment and find the highest earning segment",
        "Country where the highest number of products were sold"
    ], 
    index=0  
)

# Display selected options
st.write(f"You selected: {option1} from the first sidebar")

# Query Dictionary
query_dict = {
    "Top 10 Revenue Products": """
        SELECT p.product_id, SUM(p.quantity * p.cost_price) AS total_revenue
        FROM orders_table o
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "Top 5 Cities with Highest Profit": """ 
        SELECT 
            o.city, 
            SUM((p.sale_price - p.cost_price) * p.quantity) AS total_margin 
        FROM orders_table o
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.city
        ORDER BY total_margin DESC
        LIMIT 5;
    """,
    "Total Discount per Category": """
        SELECT category, SUM(discount) AS total_discount
        FROM products_table 
        GROUP BY category
        ORDER BY total_discount DESC;
    """,
    "Average sale price per product Category": """
        SELECT category, AVG(sale_price) AS avg_sale_price
        FROM products_table 
        GROUP BY category
        ORDER BY avg_sale_price DESC;
    """,
    "Average sale price by highest region": """
        SELECT o.region, AVG(p.sale_price) AS avg_sale_price
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.region
        ORDER BY avg_sale_price DESC
        LIMIT 1;
    """,
    "Total profit per category": """
        SELECT category, SUM(profit) AS total_profit
        FROM products_table 
        GROUP BY category
        ORDER BY total_profit DESC;
    """,
    "Top 3 segments highest quantity of orders": """
        SELECT o.segment, SUM(p.quantity) AS total_quantity
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    """,
    "Determine the avg discount percentage given per region": """
        SELECT o.region, AVG(p.discount_percent) AS avg_discount_percent
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.region;
    """,
    "Product category with the highest total profit": """
        SELECT sub_category, SUM(profit) AS total_profit
        FROM products_table 
        GROUP BY sub_category
        ORDER BY total_profit DESC;
    """,
    "Total revenue generated per year": """
        SELECT YEAR(o.order_date) AS year, SUM(p.sale_price * p.quantity) AS total_revenue
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY year
        ORDER BY year;
    """,
    "Total number of unique products sold per region": """
        SELECT o.region, COUNT(DISTINCT p.product_id) AS unique_products_sold
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.region;
    """,
    "Top 5 states with total discount": """
        SELECT o.state, SUM(p.discount) AS total_discount
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.state
        ORDER BY total_discount DESC
        LIMIT 5;
    """,
    "Total profit for each sub category":"""
        SELECT p.sub_category, SUM(p.profit) AS total_profit
        FROM products_table p 
        GROUP BY p.sub_category
        ORDER BY total_profit DESC;
    """,
    "Average sale price per product per city": """
        SELECT o.city, p.product_id, AVG(p.sale_price) AS avg_sale_price
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.city, p.product_id
        ORDER BY avg_sale_price DESC;
    """,
    "Determine the region with the highest total number of orders":"""
        SELECT o.region, COUNT(o.order_id) AS total_orders
        FROM orders_table o 
        GROUP BY o.region
        ORDER BY total_orders DESC
        LIMIT 1;
    """,
    "Top 3 categories that contributed to the highest total revenue":"""
        SELECT p.category, SUM(p.sale_price * p.quantity) AS total_revenue
        FROM products_table p
        GROUP BY p.category
        ORDER BY total_revenue DESC
        LIMIT 3;
  """,
  "Top 5 customers city wise with the highest order count":"""
        SELECT o.city, COUNT(o.order_id) AS total_orders
        FROM orders_table o 
        GROUP BY o.city
        ORDER BY total_orders DESC
        LIMIT 5;
    """,
    "Percentage of orders that used each ship mode":"""
        SELECT o.ship_mode, COUNT(o.order_id) * 100.0/ (SELECT COUNT(*) FROM orders_table) AS percentage_of_orders
        FROM orders_table o 
        GROUP BY o.ship_mode;
    """,
    "Total revenue per segment and find the highest earning segment":"""
        SELECT o.segment, SUM(p.sale_price * p.quantity) AS total_revenue
        FROM orders_table o
        JOIN products_table p ON o.order_id=p.order_id
        GROUP BY o.segment
        ORDER BY total_revenue DESC
        LIMIT 5;
""",
    "Country where the highest number of products were sold": """
        SELECT o.country, SUM(p.quantity) AS total_products_sold
        FROM orders_table o 
        JOIN products_table p ON o.order_id = p.order_id
        GROUP BY o.country
        ORDER BY total_products_sold DESC;
    """
}

# Fetch Data Based on Selection
if option1 in query_dict:
    query = query_dict[option1]
    df_result1 = pd.read_sql(query, engine)
    st.subheader(f"Results for: {option1}")
    st.dataframe(df_result1)

st.write(f"You selected: {option2} from the second sidebar")
if option2 in query_dict:
    query = query_dict[option2]
    df_result2 = pd.read_sql(query, engine)
    st.subheader(f"Results for: {option2}")
    st.dataframe(df_result2)

