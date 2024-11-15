import streamlit as st
import connection as cn
from cryptography.fernet import Fernet


if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    
def login():
    st.header("Login Page Fernet Decryption with Key")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Query data
        query = cn.run_query(query="SELECT * FROM users;")
        # Print results
        if query is not None and not query.empty:
            for row in query.itertuples():
                key = row.fernetkey
                fernet = Fernet(key.encode()) # encode to convert string to bytes
                decPass = fernet.decrypt(row.password).decode() 
                if(username == row.username and password == decPass):
                    st.session_state["is_logged_in"] = True  # Set login flag to True
                    st.session_state["username"] = username  # Optional: store username
                    st.rerun()  # Rerun the script to update the UI
                    return 
                if(row.Index == len(query.index) - 1):
                    st.error("Login failed. Please check your credentials.")

        else:
            st.write("No data found.")


if __name__ == "__main__":
    login()
    # Check login status and redirect to Dashboard if logged in
    if st.session_state["is_logged_in"]:
        st.write("Redirecting to Dashboard...")