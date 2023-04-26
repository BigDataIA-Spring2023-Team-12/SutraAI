import sqlite3
import hashlib
import streamlit as st
from google.oauth2 import service_account
import pandas as pd
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import textract
import PyPDF2
from io import BytesIO
from PIL import Image

# Connect to SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Set up the OAuth flow
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
FLOW = Flow.from_client_secrets_file(
    "client_secret.json",
    scopes=SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob",
)


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
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    queries TEXT,
                    FOREIGN KEY(username) REFERENCES users(username)
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


@st.cache_data(experimental_allow_widgets=True)
def get_gdrive_service():
    """Fetches or builds and returns a Google Drive API service instance using a service account credentials file.

    Returns:
        An instance of the Google Drive API service with version v3.

    Raises:
        HttpError: If an error occurs while building the API service instance.
    """

    creds = st.session_state.get("creds")
    if not creds or not creds.valid:
        # If there are no (valid) credentials available, let the user log in.
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        st.session_state["creds"] = creds

    # Build the Google Drive API service instance
    service = build('drive', 'v3', credentials=creds)
    return service


@st.cache_data  # (allow_output_mutation=True)
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


def log_queries(user, query):
    c.execute("INSERT INTO history (username, queries) VALUES (?,?)", (user, query))
    conn.commit()


def get_search_history(user):
    c.execute("SELECT queries FROM history WHERE username=?", (user,))
    results = c.fetchall()
    return results


@st.cache_data(experimental_allow_widgets=True)
def get_credentials():
    """
    Retrieve or generate credentials and store them in Streamlit's cache.
    """
    creds = st.session_state.get("creds")
    if not creds or not creds.valid:
        # If there are no (valid) credentials available, let the user log in.
        # st.warning("Please log in to your Google account.")
        auth_url, _ = FLOW.authorization_url(prompt="consent")
        # Open the authorization URL in the browser and wait for the user to authenticate
        st.write("Trouble Authentiating?")
        if st.button("Authorize with Code"):
            st.markdown(f"[Get Authentication Code]({auth_url})")

            auth_code = st.text_input("Enter the authorization code:")
            if auth_code:
                st.write("You entered: ", auth_code)
                token = FLOW.fetch_token(authorization_response=auth_code)
                creds = Credentials.from_authorized_user_info(info=token)
                # st.session_state["creds"] = creds
                # st.success("Authorized successfully!")

        st.session_state["creds"] = creds
        st.success("Authorized successfully!")

    service = get_gdrive_service()
    return service


@st.cache_data(experimental_allow_widgets=True)
def list_files_in_drive():
    """
    Lists the folders and files in the user's Google Drive and displays them on Streamlit.
    """

    service = get_credentials()

    query = "mimeType='application/vnd.google-apps.folder' or mimeType!='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get("files", [])

    st.header("Files in Google Drive")
    if not items:
        st.write("No files or folders found in your Google Drive.")
    else:
        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder":
                st.write(f"Folder: {item['name']}")
            else:
                st.write(f"File: {item['name']}")


@st.cache_data(experimental_allow_widgets=True)
def display_files_in_drive():
    """
    Shows the folders and files in the user's Google Drive and allows the user to open the file in Streamlit.
    """
    st.header("Files in Google Drive")
    service = get_credentials()
    # query = "mimeType='application/vnd.google-apps.folder' or mimeType!='application/vnd.google-apps.folder'"
    query = "trashed = false and mimeType!='application/vnd.google-apps.folder'"

    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get("files", [])

    if not items:
        st.write("No files or folders found in your Google Drive.")
    else:
        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder":
                st.write(f"Folder: {item['name']}")
            else:
                st.write(f"File: {item['name']}")
                if st.button(f"Open {item['name']}", key=f"button_{item['id']}"):
                    file_id = item["id"]
                    download_url = f"https://drive.google.com/uc?id={file_id}"
                    with st.spinner(f"Downloading {item['name']}..."):
                        content = requests.get(download_url).content
                    st.write("Download finished!")
                    st.write(f"Showing {item['name']}:")
                    img_buffer = io.BytesIO(content)
                    image = Image.open(img_buffer)
                    st.image(image, caption=item['name'], use_column_width=True)


@st.cache_data
def get_file_data(file_id):
    """
    Downloads a file from Google Drive and returns its contents as bytes.
    """
    drive_service = get_gdrive_service()
    file = drive_service.files().get(fileId=file_id, fields="id, name, mimeType, size").execute()

    if "application/pdf" in file["mimeType"]:
        # For PDF files, read the raw bytes of the file
        file_bytes = drive_service.files().get_media(fileId=file_id).execute()
        return file["name"], file_bytes

    elif "application/vnd.google-apps.document" in file["mimeType"]:
        # For Google Docs files, export to plain text format and read the text
        export_mimetype = "text/plain"
        file_bytes = drive_service.files().export(fileId=file_id, mimeType=export_mimetype).execute()
        return file["name"], file_bytes.encode("utf-8")

    else:
        st.warning(f"Unsupported file type: {file['mimeType']}")
        return None
    # """
    # Downloads the content of a file from Google Drive given its ID.
    # Returns the file name and data.
    # """
    # drive_service = get_gdrive_service()
    # file = drive_service.files().get(fileId=file_id).execute()
    # file_name = file['name']
    # export_mime_types = {
    #     'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    #     'application/vnd.google-apps.spreadsheet': 'text/csv'
    # }
    # if file['mimeType'] in export_mime_types:
    #     export_type = export_mime_types[file['mimeType']]
    #     export_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType={export_type}'
    #     response = drive_service.files().export(fileId=file_id, mimeType=export_type).execute()
    #     file_data = response.encode('utf-8')
    # elif file['mimeType'] == 'application/pdf':
    #     file_data = drive_service.files().get_media(fileId=file_id).execute()
    # else:
    #     file_data = None
    # return file_name, file_data


# def process_file():
#     """
#     Allows the user to select a file from their Google Drive account and downloads it as plain text.
#     """
#     drive_service = get_gdrive_service()

#     # Get a list of the user's files from Google Drive
#     results = drive_service.files().list(
#         pageSize=1000,
#         fields="nextPageToken, files(id, name, mimeType)"
#     ).execute()
#     files = results.get("files", [])

#     with st.form(key="select a file"):    
#         # Create a select box that allows the user to choose a file
#         selected_file = st.selectbox("Select a file", files, format_func=lambda file: file["name"])
#         submit_button = st.form_submit_button("Process")


#     if selected_file and submit_button:
#         # # Download the selected file as plain text
#         # file_id = selected_file["id"]
#         # file_name, file_data = get_file_data(file_id)
#         # if file_data:
#         #     # Encode the file data as plain text
#         #     file_text = file_data.decode("utf-8")
#         # Encode the file data as plain text

#         # Download the selected file as plain text
#         file_id = selected_file["id"]
#         file_name, file_data = get_file_data(file_id)
#         if file_data:
#             if file_name.endswith(('.docx', '.txt', '.pdf', '.csv')):
#                 file_text = file_data.decode("utf-8")
#             else:
#                 file_text = textract.process(BytesIO(file_data)).decode("utf-8")

#             # Download the plain text file
#             b64_data = base64.b64encode(file_text.encode("utf-8")).decode("utf-8")
#             href = f'<a href="data:text/plain;base64,{b64_data}" download="{file_name}">Download plain text file</a>'
#             st.markdown(href, unsafe_allow_html=True)
#         else:
#             st.warning("Could not retrieve file data.")


def process_file():
    """
    Allows the user to select a file from their Google Drive account and displays it as a preview.
    """
    drive_service = get_gdrive_service()

    # Get a list of the user's files from Google Drive
    results = drive_service.files().list(
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    files = results.get("files", [])

    with st.form(key="select a file"):
        # Create a select box that allows the user to choose a file
        selected_file = st.selectbox("Select a file", files, format_func=lambda file: file["name"])
        submit_button = st.form_submit_button("Process")

    if selected_file and submit_button:
        # Download the selected file and display it as a preview
        file_id = selected_file["id"]
        file_name, file_data = get_file_data(file_id)
        if file_data:
            if file_name.endswith(('.docx', '.txt', '.pdf', '.csv')):
                if file_name.endswith('.csv'):
                    df = pd.read_csv(BytesIO(file_data))
                    st.write(df)
                elif file_name.endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfFileReader(BytesIO(file_data))
                    pages = pdf_reader.getNumPages()
                    for i in range(pages):
                        page = pdf_reader.getPage(i)
                        st.write(page.extractText())
                else:
                    st.write(file_data.decode("utf-8"))
            else:
                try:
                    file_text = textract.process(BytesIO(file_data)).decode("utf-8")
                    st.write(file_text)
                except:
                    st.warning("Could not display file preview.")
        else:
            st.warning("Could not retrieve file data.")
