import streamlit as st
import bcrypt
from utils import db

def login_register():
    if "user" not in st.session_state:
        st.session_state.user = None

    menu = st.sidebar.radio("Menu", ["Login", "Register"])
    if menu == "Login":
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")
        if login_submit:
            user_record = db.get_user(username)
            if user_record is None:
                st.sidebar.error("User does not exist")
            else:
                stored_hashed = user_record[2]
                if bcrypt.checkpw(password.encode(), stored_hashed.encode()):
                    st.session_state.user = username
                    st.sidebar.success(f"Logged in as {username}")
                else:
                    st.sidebar.error("Invalid password")
    elif menu == "Register":
        with st.sidebar.form("register_form"):
            new_username = st.text_input("New Username", key="new_username")
            new_password = st.text_input("New Password", type="password", key="new_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            register_submit = st.form_submit_button("Register")
        if register_submit:
            if new_password != confirm_password:
                st.sidebar.error("Passwords do not match")
            else:
                if db.get_user(new_username) is not None:
                    st.sidebar.error("Username already exists")
                else:
                    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                    db.register_user(new_username, hashed.decode())
                    st.sidebar.success("Registration successful! Please login.")
    return st.session_state.user
