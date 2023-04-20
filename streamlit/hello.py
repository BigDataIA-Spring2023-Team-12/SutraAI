import streamlit as st
import sqlite3
import hashlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set page title and layout
st.set_page_config(page_title="SutraAI", layout="wide")

# Connect to SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Create users table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )""")

# Create a sidebar menu for user registration and login
menu_options = ["User Registration", "User Login"]
menu_selection = st.sidebar.selectbox("Select an option", menu_options)

# Register a new user
if menu_selection == "User Registration":
    st.sidebar.header("User Registration")
    new_username = st.sidebar.text_input("Enter a new username")
    new_password = st.sidebar.text_input("Enter a new password", type="password")
    if st.sidebar.button("Create User"):
        c.execute("SELECT * FROM users WHERE username=?", (new_username,))
        result = c.fetchone()
        if result:
            st.sidebar.error("Username already taken. Please choose a different username.")
        else:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (new_username, password_hash))
            conn.commit()
            st.sidebar.success("User created successfully.")

# Log in an existing user
elif menu_selection == "User Login":
    st.sidebar.header("User Login")
    existing_username = st.sidebar.text_input("Enter your username")
    existing_password = st.sidebar.text_input("Enter your password", type="password")
    if st.sidebar.button("Log In"):
        c.execute("SELECT password_hash FROM users WHERE username=?", (existing_username,))
        result = c.fetchone()
        if result:
            password_hash = hashlib.sha256(existing_password.encode()).hexdigest()
            if password_hash == result[0]:
                st.sidebar.success("Login successful!")
                st.session_state.username = existing_username
            else:
                st.sidebar.error("Incorrect password.")
        else:
            st.sidebar.error("Username not found.")

# Check if user is logged in
if "username" in st.session_state:
    st.write(f"You are logged in as {st.session_state.username}.")

    # Google Drive OAuth button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Connect to Google Drive")
    with col2:
        if st.button("Connect"):
            try:
                service = get_gdrive_service()
                st.success("Successfully connected to Google Drive!")
            except HttpError:
                st.error("Unable to connect to Google Drive.")

    # Query section title
    st.header("Query Important Information")

    # Text box for user input
    query = st.text_input("Enter your query here")

    # Submit button
    if st.button("Search"):
        try:
            # TODO: implement search functionality using query and Google Drive API
            results = []
            st.write(results)
        except HttpError:
            st.error("Unable to retrieve search results.")
else:
    st.warning("Please log in to access Google Drive and search functionality.")

# Close database
conn.close()
