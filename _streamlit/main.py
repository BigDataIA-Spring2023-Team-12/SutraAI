import streamlit as st
import os
from googleapiclient.errors import HttpError
from _utils import display_files_in_drive, process_file, get_file_id,get_creds
from load_from_drive import extract_text_from_file
from google_auth_oauthlib.flow import Flow


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Set up the OAuth flow
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FLOW = Flow.from_client_secrets_file(
    "client_secret.json",
    scopes=SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob",
)



def main():
    md_text = '''
    # 🚀 SutraAI: Building a Smart Query Tool for Querying Multiple Documents 📚
     
     👋 In today's world, there is a lot of textual data present in various formats, and accessing the required information from this data can be a challenging task. The proposed project aims to build a 🔍 smart query tool that can query multiple documents and retrieve the relevant information based on user input queries. 
    '''

    # Set page title and layout
    st.set_page_config(page_title="SutraAI", layout="wide")

    # create_users_table()

    menu_selection = st.sidebar.selectbox("Select an option", ["Home", "Access Drive"])

    if menu_selection == "Home":
        st.markdown(md_text)

    elif menu_selection == "Access Drive":

        st.header("Connect to Google Drive")
        selection = st.selectbox("Select an action", ["Select an option", "Display Files", "Display Content","Extract text from files"])

        if selection == "Display Files":
            display_files_in_drive()
        elif selection == "Display Content":
            process_file()

        elif selection == "Extract text from files":
            file_id = get_file_id()
            st.write("File ID before function call:", file_id)
            credentials = get_creds()
            # flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            st.write("Creds before function call:", credentials)
            text = extract_text_from_file(file_id, credentials)
            st.write("TEXT:", text)

            
        st.markdown("---")
        st.header("Query Important Information")

        # Text box for user input
        query = st.text_input("Enter your query here")
        

        # Submit button
        if st.button("Search"):
            try:
                # log_queries(user,query)

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
