import streamlit as st
from list_pages import Login_Page, Register_Page, Dashboard

if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if st.session_state['is_logged_in']:
    st.sidebar.title("Kristography Navigation")
    username = st.session_state['username']
    st.sidebar.success(f"Logged in as {username}")
    page = st.sidebar.selectbox("Go to", ["Kotak Pandora", "Galeri Stegano", "Hermest Chest"], format_func=lambda x: f"📦 {x}" if x == "Kotak Pandora" else f"🖼️ {x}" if x == "Galeri Stegano" else f"📁 {x}")
    Dashboard.dashboard(page)
    if st.sidebar.button("Logout"):
        st.session_state['is_logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
   
else:
    with st.sidebar:
        st.sidebar.title("Kristography Navigation")
        st.sidebar.warning("Not logged in")
        page = st.sidebar.selectbox("Go To", ["Login", "Register"], format_func=lambda x: f"🔒 {x}" if x == "Login" else f"📝 {x}")
        
    if page == "Login":
        Login_Page.login()
    elif page == "Register":
        Register_Page.register()
