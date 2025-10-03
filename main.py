import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# ...existing code...
from google.cloud import bigquery
from google.cloud import storage
import os
from pathlib import Path
import streamlit as st

# Load environment variables from a .env file (if present)
# We'll use python-dotenv if available but keep working if it's not installed.
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except Exception:
    # python-dotenv not installed; environment variables must be set externally
    pass

# Set up Google Cloud credentials: prefer existing environment variable, otherwise you
# can put GOOGLE_APPLICATION_CREDENTIALS in a .env file at the project root.
creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
if not creds:
    # Optionally set a default path (commented out). It's better to set via .env or OS env.
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\path\to\your\credentials.json"
    raise RuntimeError(
        'GOOGLE_APPLICATION_CREDENTIALS is not set. Put the JSON path in a .env file or set the environment variable.'
    )

# Initialize BigQuery and Storage clients
client = bigquery.Client()
storage_client = storage.Client()

st.title("Retail Store Analysis")

radio = st.radio("Select the table to view", ("customers", "geolocation", "order_items", "order_reviews", "orders", "payments", "sellers", "products"))
if radio == "customers":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'customers'"""
elif radio == "customers":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'customers'"""
elif radio == "geolocation":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'geolocation'"""
elif radio == "order_items":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'order_items'"""
elif radio == "order_reviews":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'order_reviews'"""
elif radio == "orders":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'orders'"""
elif radio == "payments":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'payments'"""
elif radio == "sellers":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'sellers'"""
elif radio == "products":
    query1 = f"""
    SELECT table_catalog AS project, table_schema, table_name, column_name, data_type, is_nullable 
    FROM `project1-ai-lab-sql.retail.INFORMATION_SCHEMA.COLUMNS`
    WHERE table_name = 'products'"""


st.header("", divider="blue")
# Display dataframe in Streamlit
st.text("Data type of all columns in the customers table details on the selected table",)
st.code(query1  , language='sql')
st.dataframe(client.query(query1).to_dataframe())


st.header("", divider="blue")
st.text("Get the time range between which the orders were placed.")

query2 = """
SELECT EXTRACT(DATE FROM MIN(order_purchase_timestamp)) AS `first order date`, 
FORMAT_DATE('%A', EXTRACT(DATE FROM MIN(order_purchase_timestamp))) AS `first order day of the week`,
EXTRACT(TIME FROM MIN(order_purchase_timestamp)) AS `first order time`, 
EXTRACT(DATE FROM MAX(order_purchase_timestamp)) AS `last order date`,
FORMAT_DATE('%A', EXTRACT(DATE FROM MAX(order_purchase_timestamp))) AS `last order day of the week`,
EXTRACT(TIME FROM MAX(order_purchase_timestamp)) AS `last order time`
FROM `project1-ai-lab-sql.retail.orders`"""

st.code(query2  , language='sql')
st.dataframe(client.query(query2).to_dataframe())

st.header("", divider="blue")
st.text("Count the Cities & States of customers who ordered during the given period.")

query3 = """
SELECT COUNT(DISTINCT customer_state) AS `customer_state`,COUNT(DISTINCT customer_city) As customer_city
FROM `project1-ai-lab-sql.retail.customers`
"""

st.code(query3  , language='sql')
st.dataframe(client.query(query3).to_dataframe())

st.header("", divider="blue")
st.text("Is there a growing trend in the no. of orders placed over the past years?")

query4 = """
SELECT COUNT(DISTINCT customer_state) AS `customer_state`,COUNT(DISTINCT customer_city) As customer_city
FROM `project1-ai-lab-sql.retail.customers`
"""

st.code(query4  , language='sql')
st.dataframe(client.query(query4).to_dataframe())
