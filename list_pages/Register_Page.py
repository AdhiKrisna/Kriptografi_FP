import streamlit as st
import connection as cn
from cryptography.fernet import Fernet

def register():
    st.header("Register Page (Fernet Encryption)")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encPass = fernet.encrypt(password.encode()).decode() # decode() to convert bytes to string biar bisa masukin ke database varchar
        # decPass = fernet.decrypt(encPass).decode()  
        
        # st.write(key)
        # st.write(fernet)
        # st.write(f"Password: {password}")
        # st.write(f"Encrypted password: {encPass}")
        # st.write(f"Decrypted password: {decPass}")

        query = cn.run_query("SELECT * FROM users WHERE username = '" + username + "';", fetch=True)
        if query.empty:
            cn.run_query("INSERT INTO users (username, password, fernetKey) VALUES ('" + username + "', '" + encPass + "' , '" + key.decode() + "');", fetch=False) # key decode() to convert bytes to string
            st.success(f"User with username '{username}' has been registered successfully. You can now login.")
        else:
            st.error("Username already exists.")

if __name__ == "__main__":
    register()