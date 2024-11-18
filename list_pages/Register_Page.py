import streamlit as st
import connection as cn
from cryptography.fernet import Fernet
import app as app

def register():
    col1, col2, col3 = st.columns([10, 1, 3])
    with col1:
        st.title(":green[Welcome to Kristography]")
        st.header(":red[Register Here...]")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if username == "" or password == "":
                st.error("Please fill in all fields.")
                st.stop()
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encPass = fernet.encrypt(password.encode()).decode() # decode() to convert bytes to string biar bisa masukin ke database text

            query = cn.run_query("SELECT * FROM users WHERE username = '" + username + "';", fetch=True)
            if query.empty:
                query = "INSERT INTO users (username, password, fernetkey) VALUES (%s, %s, %s);"
                params = (username, encPass, key.decode())
                cn.run_query(query, params, fetch=False)
                st.success(f"User with username '{username}' has been registered successfully. You can now login.")
                app.page = "Login"
                st.rerun()
            else:
                st.error("Username already exists.")
    with col2:
        None
    with col3:
        st.image("assets/gambar.png", width=200)

if __name__ == "__main__":
    register()