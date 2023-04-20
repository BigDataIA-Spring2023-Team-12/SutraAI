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

# Page title
st.title("SutraAI")

# User registration section title
st.header("User Registration")

# Text box for new username
new_username = st.text_input("Enter a new username:")

# Password input field
new_password = st.text_input("Enter a new password:", type="password")

# Button to create new user
if st.button("Create User"):
    # Check if username is already taken
    c.execute("SELECT * FROM users WHERE username=?", (new_username,))
    result = c.fetchone()
    if result:
        st.error("Username already taken. Please choose a different username.")
    else:
        # Hash password using SHA-256 algorithm
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        # Add new user to database
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (new_username, password_hash))
        conn.commit()

        st.success("User created successfully.")

# User login section title
st.header("User Login")

# Text box for existing username
existing_username = st.text_input("Enter your username:")

# Password input field for existing user
existing_password = st.text_input("Enter your password:", type="password")

# Button to log in user
if st.button("Log In"):
    # Retrieve hashed password from database for the given username
    c.execute("SELECT password_hash FROM users WHERE username=?", (existing_username,))
    result = c.fetchone()
    if result:
        # Hash the input password and compare it with the stored hash
        password_hash = hashlib.sha256(existing_password.encode()).hexdigest()
        if password_hash == result[0]:
            st.success("Login successful!")
            # Set a session variable to track the logged in user
            st.session_state.username = existing_username
        else:
            st.error("Incorrect password.")
    else:
        st.error("Username not found.")

# Check if user is logged in
if "username" in st.session_state:
    # Google Drive OAuth button
    @st.cache(allow_output_mutation=True)
    def get_gdrive_service():
        credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
        return build('drive', 'v3', credentials=credentials)

    if st.button("Connect Google Drive"):
        try:
            service = get_gdrive_service()
            st.success("Successfully connected to Google Drive!")
        except HttpError:
            st.error("Unable to connect to Google Drive.")

    # Query section title
    st.header("Query Important Information")

    # Text box for user input
    query = st.text_input("Enter your query here:")

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
