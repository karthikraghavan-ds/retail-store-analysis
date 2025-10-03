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
import tempfile
import json

# Load environment variables from a .env file (if present)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except Exception:
    # python-dotenv not installed; environment variables must be set externally
    pass


# Helper: ensure GOOGLE_APPLICATION_CREDENTIALS is set.
# Supports three patterns:
# 1) Local path in env var (GOOGLE_APPLICATION_CREDENTIALS)
# 2) JSON contents provided via env var or Streamlit secret (GOOGLE_SERVICE_ACCOUNT)
# 3) Streamlit's st.secrets dict with key GOOGLE_SERVICE_ACCOUNT
def ensure_gcloud_credentials():
    # 1) If already set and the file exists, we're done.
    gac_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if gac_path and Path(gac_path).exists():
        return

    # 2) Check for an env var containing JSON or a path
    candidate = os.environ.get('GOOGLE_SERVICE_ACCOUNT') or os.environ.get('GOOGLE_CLOUD_SERVICE_ACCOUNT')
    if candidate:
        c = candidate.strip()
        if c.startswith('{'):
            # JSON contents -> write to temp file
            fd, temp_path = tempfile.mkstemp(suffix='.json')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(c)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_path
            return
        else:
            # assume it's a path
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = c
            return

    # 3) If running in Streamlit, check st.secrets
    try:
        secrets = st.secrets
        # common secret key name: GOOGLE_SERVICE_ACCOUNT
        secret_json = None
        if isinstance(secrets, dict):
            secret_json = secrets.get('GOOGLE_SERVICE_ACCOUNT') or secrets.get('GOOGLE_CLOUD_SERVICE_ACCOUNT')
        else:
            # st.secrets supports attribute access; try both
            secret_json = getattr(secrets, 'GOOGLE_SERVICE_ACCOUNT', None) or getattr(secrets, 'GOOGLE_CLOUD_SERVICE_ACCOUNT', None)

        if secret_json:
            s = secret_json.strip()
            if s.startswith('{'):
                fd, temp_path = tempfile.mkstemp(suffix='.json')
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(s)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_path
                return
            else:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = s
                return
    except Exception:
        # st may not be available or secrets not set
        pass


# Run the helper to ensure credentials are available; if not, raise a clear error for local dev.
ensure_gcloud_credentials()

# Final check
if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    raise RuntimeError(
        'GOOGLE_APPLICATION_CREDENTIALS not configured. Locally, create a .env with the path. On Streamlit Cloud, add the service account JSON as a secret named GOOGLE_SERVICE_ACCOUNT.'
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
