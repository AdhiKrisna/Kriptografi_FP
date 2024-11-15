import mysql.connector
from mysql.connector import Error
# import psycopg2
# import pandas as pd
# import streamlit as st

# # Initialize connection
# def create_connection():
#     try:
#         connection = psycopg2.connect(
#             host=st.secrets["host"],
#             user=st.secrets["username"],
#             password=st.secrets["password"],
#             database=st.secrets["database"],
#             port=st.secrets.get("port", 5432)
#         )
#         return connection
#     except Error as e:
#         st.error(f"Error connecting to MySQL: {e}")
#         return None

# # Perform query
# def run_query(query, params=None, fetch=True):
#     """
#     Runs a SQL query with optional parameters.
    
#     - `query`: The SQL query string.
#     - `params`: Optional parameters to be passed with the query.
#     - `fetch`: If True, fetches results (used for SELECT queries).
#     """
#     conn = create_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         try:
#             if params:
#                 cursor.execute(query, params)
#             else:
#                 cursor.execute(query)
            
#             # For SELECT queries, fetch results
#             if fetch:
#                 result = cursor.fetchall()
#                 return pd.DataFrame(result) if result else pd.DataFrame()
            
#             # For INSERT, UPDATE, DELETE queries
#             else:
#                 conn.commit()
#                 return None
#         except Exception as e:
#             st.error(f"Error executing query: {e}")
#             return None
#         finally:
#             cursor.close()
#             conn.close()
#     else:
#         st.error("Failed to connect to the database.")
#         return None


import psycopg2
import pandas as pd
import streamlit as st
from psycopg2 import Error
from psycopg2.extras import DictCursor

# Initialize connection
def create_connection():
    try:
        connection = psycopg2.connect(
            host=st.secrets["host"],
            user=st.secrets["username"],
            password=st.secrets["password"],
            database=st.secrets["database"],
            port=st.secrets.get("port", 5432),
            cursor_factory=psycopg2.extras.DictCursor  # Tambahkan ini
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

# Perform query
def run_query(query, params=None, fetch=True):
    """
    Runs a SQL query with optional parameters.
    
    - `query`: The SQL query string.
    - `params`: Optional parameters to be passed with the query.
    - `fetch`: If True, fetches results (used for SELECT queries).
    """
    conn = create_connection()
    if conn:
        cursor = conn.cursor(cursor_factory=DictCursor)  # Gunakan DictCursor di sini
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # For SELECT queries, fetch results
            if fetch:
                result = cursor.fetchall()
                return pd.DataFrame(result) if result else pd.DataFrame()
            
            # For INSERT, UPDATE, DELETE queries
            else:
                conn.commit()
                return None
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        return None
