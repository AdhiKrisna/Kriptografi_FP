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
        query = cn.run_query(query="SELECT username, password, fernetkey FROM users;")
        
        # Pastikan hasil query tidak kosong
        if query is not None and not query.empty:
            for _, row in query.iterrows():
                key = row.get("fernetkey")
                fernet = Fernet(key.encode())
                
                # Mendekripsi password
                try:
                    decPass = fernet.decrypt(row['password'].encode()).decode()
                except Exception as e:
                    st.error(f"Decryption error: {e}")
                    return
                
                if username == row['username'] and password == decPass:
                    st.success("Login successful!")
                    st.session_state["is_logged_in"] = True
                    st.session_state["username"] = username
                    st.experimental_rerun()
                    return
                
            # Jika tidak ada username yang cocok
            st.error("Login failed. Please check your credentials.")
        else:
            st.error("No data found.")

if __name__ == "__main__":
    login()
    # Check login status and redirect to Dashboard if logged in
    if st.session_state["is_logged_in"]:
        st.write(f"Welcome, {st.session_state['username']}!")
        st.write("Redirecting to Dashboard...")
