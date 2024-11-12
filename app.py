import streamlit as st
from list_pages import Login_Page, Register_Page, Dashboard

if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if st.session_state['is_logged_in']:
    st.sidebar.title("Navigation")
    st.sidebar.success("Logged in")
    page = st.sidebar.selectbox("Go to", ["Message Cryptography", "Image Encrypt Stegano", "File Encrypt"])
    Dashboard.dashboard(page)
   
else:
    with st.sidebar:
        st.sidebar.title("Navigation")
        st.sidebar.warning("Not logged in")
        page = st.sidebar.selectbox("Go To", ["Login", "Register"], format_func=lambda x: f"🔒 {x}" if x == "Login" else f"📝 {x}")
    if page == "Login":
        Login_Page.login()
    elif page == "Register":
        Register_Page.register()
