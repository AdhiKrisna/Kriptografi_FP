import streamlit as st
import connection as cn
from cryptography.fernet import Fernet

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

def login():
    col1, col2, col3 = st.columns([10, 1, 3])
    with col1:
        st.title(":green[Welcome to Kristography]")
        st.header(":red[Foreigner Detected, Please Login to Continue]")
       
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Query data
            query = cn.run_query(query="SELECT username, password, fernetkey FROM users;")
            # st.write("Query Result:", query)
            # jika ada hasil query, lakukan pengecekan username dan password
            if query is not None and not query.empty:
                for _, row in query.iterrows():
                    key = row['fernetkey']
                    fernet = Fernet(key.encode())
                    
                    # Mendekripsi password
                    try:
                        decPass = fernet.decrypt(row['password'].encode()).decode() # Decode bytes to string
                    except Exception as e:
                        st.error(f"Decryption error: {e}")
                        return
                    
                    if username == row['username'] and password == decPass:
                        st.success("Login successful!")
                        st.session_state["is_logged_in"] = True
                        st.session_state["username"] = username
                        st.rerun()
                        return
                    
                # Jika tidak ada username yang cocok
            st.error("Login failed. Please check your credentials.")
        else:
            st.write(':red[Kristaleo Says: "Please Login to Continue"]')
    with col2:
        None
    with col3:
        st.image("assets/gambar.png", width=200)

if __name__ == "__main__":
    login()
    # Check login status and redirect to Dashboard if logged in
    if st.session_state["is_logged_in"]:
        st.write(f"Welcome, {st.session_state['username']}!")
        st.write("Redirecting to Dashboard...")
