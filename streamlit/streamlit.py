import sqlite3
import hashlib
import streamlit as st
from google.oauth2 import service_account
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Connect to SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

def create_users_table():
    """
    Creates the users table and history table in the database if it doesn't exist.
    """
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL
                )""")
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS history (
                    username TEXT PRIMARY KEY,
                    queries TEXT
                )""")
    conn.commit()

def register_user():
    """
    Registers a new user by inserting their username and hashed password
    into the users table in the database.
    """
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

def login_user():
    """
    Logs in an existing user by checking their entered username and
    password against the users table in the database.
    """
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



@st.cache(allow_output_mutation=True)
def get_gdrive_service():
    """Fetches or builds and returns a Google Drive API service instance using a service account credentials file.

    Returns:
        An instance of the Google Drive API service with version v3.

    Raises:
        HttpError: If an error occurs while building the API service instance.
    """
    credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json')
    try:
        service = build('drive', 'v3', credentials=credentials)
        return service
    except HttpError as error:
        st.error(f"An error occurred: {error}")


@st.cache(allow_output_mutation=True)
def upload_service():
    """Returns a Google Drive API service instance with write access to the user's Google Drive.

    Returns:
        An instance of the Google Drive API service with version v3 and write access scope.

    Raises:
        KeyError: If the Google Drive API credentials are not defined in Streamlit secrets.
    """
    try:
        creds = st.secrets["creds"]
    except KeyError:
        st.error("Google Drive API credentials not found in Streamlit secrets.")
        raise

    scope = ["https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_info(info=creds, scopes=scope)
    
    try:
        service = build("drive", "v3", credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Unable to build the Google Drive API service: {e}")




def upload_file_to_google_drive(file):
    """Uploads a file to the user's Google Drive using the specified Google Drive API service instance.

    Args:
        file: The file to upload to Google Drive.
        upload_service: The Google Drive API service instance to use for the upload.

    Returns:
        The ID of the uploaded file.

    Raises:
        HttpError: If an error occurs while creating the file in Google Drive.
    """
    try:
        # Create a file in Google Drive
        file_metadata = {"name": file.name}
        media = {"media": file}
        service = upload_service()
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return file["id"]
    except HttpError as error:
        st.error(f"An error occurred while uploading file to Google Drive: {error}")
        raise

def file_upload():
    """Runs a Streamlit app for uploading a file to Google Drive.

    Args:
        upload_service: The Google Drive API service instance to use for the upload.
    """
    file = st.file_uploader("Choose a file")
    if file is not None:
        file_id = upload_file_to_google_drive(file)
        st.success(f"File '{file.name}' uploaded successfully with file ID {file_id}.")





def log_queries(user,query):
    c.execute("INSERT INTO history (username, queries) VALUES (?,?)", (user,query))
    conn.commit()

def get_search_history(user):
    c.execute("SELECT queries FROM history WHERE username=?", (user,))
    results = c.fetchall()
    return results





def main():
    """
    Main function that runs the application.
    """

    # Set page title and layout
    st.set_page_config(page_title="SutraAI", layout="wide")
    st.write("<h1 style='text-align: center;'>SutraAI</h1>", unsafe_allow_html=True)

    st.markdown("---")

    create_users_table()

    menu_selection = st.sidebar.selectbox("Select an option", ["Home","User Registration", "User Login"])

    
    if menu_selection == "Home":
        st.write("Welcome to SutraAI!")

    elif menu_selection == "User Registration":
        register_user()
    elif menu_selection == "User Login":
        login_user()


    
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

            
        # File upload section
        st.header("File Upload")

        file_upload()

        # Query section title
        st.header("Query Important Information")

        # Text box for user input
        query = st.text_input("Enter your query here")
        user = st.session_state.username

        

        # Submit button
        if st.button("Search"):
            try:
                log_queries(user,query)

                # TODO: implement search functionality using query and Google Drive API
                
                results = []
                st.write(results)
            except HttpError:
                st.error("Unable to retrieve search results.")

        
        # Access your query history
        elif st.button("Access Search history"):
            st.header("Search history")
            history = get_search_history(user)
            history_df = pd.DataFrame(history, columns=["Past Queries"])
    
            st.dataframe(history_df)
            



    else:
        st.warning("Please log in to access Google Drive and search functionality.")




if __name__ == "__main__":
    main()
