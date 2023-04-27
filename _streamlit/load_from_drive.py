import os
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import PyPDF2
import docx2txt
from bs4 import BeautifulSoup




def extract_text_from_file(file_id: str, credentials: Credentials) -> str:

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

        # Download the file content as a bytes object
        file_content = service.files().get_media(fileId=file_id).execute()

        # Extract the text from the file content
        if file_extension == '.pdf':
            with io.BytesIO(file_content) as pdf_file:
                with PyPDF2.PdfFileReader(pdf_file) as pdf_reader:
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text()
        elif file_extension == '.json':
            text = str(file_content, 'utf-8')
        elif file_extension == '.csv':
            text = str(file_content, 'utf-8')
        elif file_extension == '.txt':
            text = str(file_content, 'utf-8')
        elif file_extension == '.doc':
            with io.BytesIO(file_content) as doc_file:
                text = docx2txt.process(doc_file)
        elif file_extension == '.docx':
            with io.BytesIO(file_content) as docx_file:
                text = docx2txt.process(docx_file)
        elif file_extension == '.odt':
            with io.BytesIO(file_content) as odt_file:
                text = str(BeautifulSoup(odt_file, 'xml').get_text())
        elif file_extension == '.html':
            with io.BytesIO(file_content) as html_file:
                text = BeautifulSoup(html_file, 'html.parser').get_text()
        else:
            text = ''

        return text

    except HttpError as error:
        raise HttpError(f"An error occurred while loading file from Google Drive: {error}")