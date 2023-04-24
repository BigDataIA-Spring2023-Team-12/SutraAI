import streamlit as st
from google.oauth2 import service_account
import pandas as pd
import os    
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import io
from PIL import Image
from utils import create_users_table,register_user,login_user,log_queries,display_files_in_drive,get_credentials,get_gdrive_service,get_search_history,file_upload,list_files_in_drive,upload_file_to_google_drive

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# MAIN FUNCTION

def main():
    """
    Main function that runs the application.
    """

        
    md_text = '''
    # 🚀 SutraAI: Building a Smart Query Tool for Querying Multiple Documents 📚

    # 👋 
    In today's world, there is a lot of textual data present in various formats, and accessing the required information from this data can be a challenging task. The proposed project aims to build a 🔍 smart query tool that can query multiple documents and retrieve the relevant information based on user input queries.

    '''

    
    # Set page title and layout
    st.set_page_config(page_title="SutraAI", layout="wide")
    st.write("<h1 style='text-align: center;'>SutraAI</h1>", unsafe_allow_html=True)

    st.markdown("---")

    # create_users_table()

    menu_selection = st.sidebar.selectbox("Select an option", ["Home","Access Drive"]) 
    
    if menu_selection == "Home":
        st.header("Welcome to SutraAI!")
        st.markdown(md_text)
        st.image("img.png")

    elif menu_selection == "Access Drive":

        st.header("Connect to Google Drive")

        if st.button("Connect and Display Files"):
            display_files_in_drive()


        st.markdown("---")

        st.header("Query Important Information")

        # Text box for user input
        query = st.text_input("Enter your query here")
           

        # Submit button
        if st.button("Search"):
            try:
                #log_queries(user,query)

                # TODO: implement search functionality using query and Google Drive API
                
                results = []
                st.write(results)
            except HttpError:
                st.error("Unable to retrieve search results.")
                    

        st.markdown("---")
       

    else:
        st.warning("Please log in to access Google Drive and search functionality.")

if __name__ == "__main__":
    main()
