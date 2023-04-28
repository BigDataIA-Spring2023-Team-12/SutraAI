import streamlit as st
import os
from googleapiclient.errors import HttpError
from _utils import get_file_text, generative_search
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
        selection = st.selectbox("Choose an option", ["Select an action","Extract text from files"])

        if selection == "Extract text from files":
            get_file_text()
            

        st.markdown("---")
        st.header("Query Important Information")

        # Text box for user input
        query = st.text_input("Enter your query here")

        # Submit button
        if st.button("Search"):
            generative_search(query)
                
            

        st.markdown("---")

    else:
        st.warning("Please log in to access Google Drive and search functionality.")


if __name__ == "__main__":
    main()
