import streamlit as st
import pandas as pd
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import textract
import PyPDF2
from io import BytesIO
from PIL import Image
import sqlite3
from datetime import datetime


# Set up the OAuth flow
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
FLOW = Flow.from_client_secrets_file(
    "client_secret.json",
    scopes=SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob",
)


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



def update_latest_refresh():
    """
    Creates or updates a SQLite database named 'latest_refresh.db' with one table named 'refresh_timestamp',
    which stores a single row containing the timestamp of the most recent click on the 'refresh' button in
    a Streamlit application.

    If the 'refresh_timestamp' table does not exist, it is created. If the table already exists, the single
    row it contains is updated with the current timestamp.

    Args:
        None

    Returns:
        None
    """
    # Create connection to database
    conn = sqlite3.connect('latest_refresh.db')
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute('CREATE TABLE IF NOT EXISTS refresh_timestamp (timestamp TEXT)')

    # Update or insert row with current timestamp
    timestamp = str(datetime.now())
    cursor.execute('SELECT COUNT(*) FROM refresh_timestamp')
    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute('INSERT INTO refresh_timestamp (timestamp) VALUES (?)', (timestamp,))
    else:
        cursor.execute('UPDATE refresh_timestamp SET timestamp=?', (timestamp,))
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()