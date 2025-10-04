import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from google.cloud import storage
import os
from pathlib import Path
import streamlit as st
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)


# Initialize BigQuery and Storage clients
client = bigquery.Client(credentials=credentials)
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
