import os
import json
import io
import zipfile
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def extract_text_from_file(file_id: str, credentials: Credentials) -> str:
    """
    Extracts text from a file in Google Drive and returns it as a string.

    Args:
        file_id (str): The ID of the file to extract text from.
        credentials (google.oauth2.credentials.Credentials): The credentials to authenticate the API request.

    Returns:
        str: The extracted text as a string.

    Raises:
        HttpError: If there was an error loading the file from Google Drive.

    """
    # Set up the OAuth flow
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    FLOW = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
)

    
    credentials = st.session_state.get("creds")
    if not credentials or not credentials.valid:
        # If there are no (valid) credentials available, let the user log in.
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        st.session_state["creds"] = credentials

    text = ''
    # Define the supported file extensions and their corresponding MIME types
    SUPPORTED_FILE_TYPES = {
        '.pdf': 'application/pdf',
        '.json': 'application/json',
        '.csv': 'text/csv',
        '.txt': 'text/plain',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.odt': 'application/vnd.oasis.opendocument.text',
        '.html': 'text/html'
    }

    try:
        # Build the Google Drive API client
        service = build('drive', 'v3', credentials=credentials)

        # Get the file metadata and content
        file = service.files().get(fileId=file_id).execute()

        # Extract the file extension and MIME type
        file_extension = os.path.splitext(file['name'])[1].lower()
        file_mime_type = file['mimeType']

        # Skip the file if it doesn't belong to the supported formats
        if file_extension not in SUPPORTED_FILE_TYPES or file_mime_type != SUPPORTED_FILE_TYPES[file_extension]:
            return ''

        # Extract the text from the file content
        if file_mime_type == 'application/pdf':
            pdf_data = service.files().export(fileId=file_id, mimeType='application/pdf').execute()
            import PyPDF2
            with PyPDF2.PdfFileReader(io.BytesIO(pdf_data)) as pdf_reader:
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
        elif file_mime_type == 'application/json':
            json_data = service.files().get_media(fileId=file_id).execute()
            text = json.dumps(json_data)
        elif file_extension == '.doc':
            doc_data = service.files().export(fileId=file_id,
                                              mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document').execute()
            import docx2txt
            with zipfile.ZipFile(io.BytesIO(doc_data)) as doc_zip:
                text = docx2txt.process(io.BytesIO(doc_zip.read('word/document.xml')).decode('utf-8'))
        elif file_extension == '.docx':
            docx_data = service.files().get_media(fileId=file_id).execute()
            import docx2txt
            with zipfile.ZipFile(io.BytesIO(docx_data)) as docx_zip:
                text = docx2txt.process(io.BytesIO(docx_zip.read('word/document.xml')).decode('utf-8'))
        elif file_extension == '.html':
            html_data = service.files().get_media(fileId=file_id).execute()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_data, 'html.parser')
            text = soup.get_text()
        else:
            text = service.files().get_media(fileId=file_id).decode('utf-8')

        st.write("TEXT:", text)
        return text

    except HttpError as error:
        raise HttpError(f"An error occurred while loading file from Google Drive: {error}")
