import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st

# Initialize connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["host"],
            user=st.secrets["username"],
            password=st.secrets["password"],
            database=st.secrets["database"]
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
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
        cursor = conn.cursor(dictionary=True)
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
        except mysql.connector.Error as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        return None
