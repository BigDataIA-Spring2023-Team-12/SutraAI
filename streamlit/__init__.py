import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set page title and layout
st.set_page_config(page_title="SutraAI", layout="wide")

# Page title
st.title("SutraAI")

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
