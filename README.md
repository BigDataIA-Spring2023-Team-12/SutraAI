# 🚀 SutraAI: Building a Smart Query Tool for Querying Multiple Documents 📚

## 👋 Introduction
In today's world, there is a lot of textual data present in various formats, and accessing the required information from this data can be a challenging task. The proposed project aims to build a 🔍 smart query tool that can query multiple documents and retrieve the relevant information based on user input queries.

## 🎯 Objectives:
The primary objectives of this project are to:
- 🏗️ Develop a backend that connects to Google Drive and allows users to upload their files and transcripts.
- 🤖 Build vector embeddings and indexing on the textual data for efficient querying.
- 🔎 Retrieve the relevant context from the data based on user input queries.
- 🧠 Use GPT-3 for summarization, phrasing, and question-answering to provide the user with a concise and accurate response.

## 📝 Methodology
The following steps will be followed to achieve the project objectives:
- Build a backend that connects to Google Drive and allows users to upload their files and transcripts. The backend will also provide an API for data retrieval.
- Develop vector embeddings and indexing on the textual data to improve the efficiency of querying.
- Use the vector embeddings and indexing to retrieve the relevant context from the data based on user input queries.
- Use GPT-3 to summarize the retrieved context and provide a concise and accurate response to the user's query. GPT-3 will also be used for phrasing and question-answering to provide a more natural language response.
- Build a user interface that allows the user to input queries and displays the relevant response.

##  Architecture
![SutraAI drawio](https://user-images.githubusercontent.com/114712818/235237787-91f48373-3533-441c-a390-5d95b7ddae66.png)


## Links
* Codelab Documentation - [Codelab](https://codelabs-preview.appspot.com/?file_id=1D1PtKea5EFGK7fB0Pct4My99E5_3xuOsEsCMHKwImgk#0)
* GitHub Repository - [GitHub](https://github.com/BigDataIA-Spring2023-Team-12/SutraAI)
* FastAPI Doc - [FastAPI](http://54.86.128.1:8000/docs)
* Application - [Streamlit](https://github.com/BigDataIA-Spring2023-Team-12/SutraAI)

##  Technical Documentation
### Project Root
- `README.md`: The main documentation file for the project.
- `gitignore`: The file containing the list of packages to exclude on git push.
- `requirements.txt`: The file containing the list of dependencies required for the project.

### _fastapi folder
- `Dockerfile`: This code sets up a Docker container with a FastAPI application that runs on port 8000.
- `embeddings.py`: This code generates embeddings for a list of sentence chunks using the all-mpnet-base-v2 model from SentenceTransformers, along with metadata in Pinecone format. It also includes a function to generate embeddings for a single sentence.
- `main.py`: This code defines a FastAPI app with endpoints to generate and search embeddings using Pinecone, preprocess input text, and handle HTTP requests for upserting vectors and performing vector search.
- `pinecone_utils`: This code provides utility functions for working with Pinecone, a vector search service, including creating embeddings with OpenAI's GPT-3 model, initializing and upserting vectors to an index, and searching an index.
- `preprocessor`: This Python function preprocesses input text by performing sentence splitting, stop word removal, and lemmatization, and returns a list of preprocessed sentence chunks.
- `requirements.txt`: This is a list of Python packages and their versions that are required for FastAPI to run.
- `text_extractor`: This function extracts text from various file formats and returns it as a string. The supported file formats are PDF, JSON, CSV, TXT, DOC, ODT, and HTML. If the file format is not supported, a ValueError is raised.
- `vector_search`: This code provides a Python script for generating responses to user queries using GPT-3.5 model and a search index created using Pinecone API, and can be used for various natural language processing applications.

### _streamlit folder
- `gitignore`: The file containing the list of packages to exclude on git push.
- `_utils.py`: This script fetches text from files in a specific Google Drive folder named 'SutraAI', and sends the text and filename to a FastAPI endpoint for further processing. The script also stores information about the processed files in a SQLite database. The user is required to provide valid credentials for Google Drive API authentication.
- `load_from_drive`: This Python script defines a function named "extract_text_from_file" which takes in a Google Drive file ID and user credentials, and returns the extracted text from the file in string format. It supports various file formats including PDF, JSON, CSV, TXT, DOC, DOCX, ODT, and HTML.
- `main.py`: This Python script uses Streamlit to create a web app that allows users to authenticate with Google Drive and extract text from files, as well as search for information using natural language queries. It uses the Google Drive API and OAuth2 authentication.
- `users.db`: User Logs.

## Testing
### Fastapi testing
- The `test_generate_embedding` function tests the `generate_embedding` function from the `_fastapi.embeddings` module. It takes in a list of sentence chunks and a filename, and it tests that the expected output is generated.
- The `test_upsert` function tests the `/upsert` endpoint of a web service running on `localhost:8000`. It sends a POST request to the endpoint with some data and tests that the response contains the expected data.
- The `TestPineconeUtils` class contains several tests for the `PineconeUtils` class from the `_fastapi.pinecone_utils module`. It tests that the class methods return the expected types of objects.
- The `test_preprocess_and_chunk` function tests the `preprocess_and_chunk` function from the `_fastapi.preprocessor` module. It tests that the function properly preprocesses and chunks text.
- The `test_extract_text_from_file` function tests the `extract_text_from_file` function from the `_fastapi.text_extractor` module. It tests that the function properly extracts text from files of various types.

### NLP testing:
- This is a script that tests the functionality of three functions: `generate_embedding`, `preprocess_and_chunk`, and `extract_text_from_file`, and prints a message indicating that all test cases have passed. 

### Streamlit testing:
- The `test_create_users_table` function tests if the function `create_users_table` is able to create the 'users' table in the database.
- The `test_register_user` function tests if the function `register_user` is able to add a new user to the 'users' table in the database.
- The `test_login_user` function tests if the function `login_user` is able to correctly set the session state variable username when a user logs in.
- The `test_log_queries` function tests if the function `log_queries` is able to add a new query to the 'history' table in the database.
- The `test_get_search_history` function tests if the function `get_search_history` is able to retrieve the search history for a particular user from the 'history' table in the database.
- The `test_get_credentials` function tests if the function `get_credentials` is able to retrieve valid Google Drive API credentials.
- The `test_list_files_in_drive` function tests if the function `list_files_in_drive` is able to correctly list the files in the user's Google Drive and print the output to the Streamlit app. This function uses a mock service object to simulate the results of the Google Drive API.






## 👉 Conclusion
The proposed project aims to build a smart query tool that can query multiple documents and retrieve the relevant information based on user input queries. The project will use Google Drive, vector embeddings, indexing, and GPT-3 to achieve this objective. The project will be completed in 2 weeks. The deliverables of the project will be a functional query tool with a user interface. 💻




---
## Team Members
1. Harsh Shah - NUID: 002704406 - (shah.harsh7@northeastern.edu)
2. Parva Shah - NUID: 002916822 - (shah.parv@northeastern.edu)
3. Dev Shah - NUID: 002978981 - (shah.devs@northeastern.edu)



## Undertaking

> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
**Contribution**: 
*   Harsh Shah &emsp; :`33.33%`
*   Parva Shah &emsp; :`33.33%`
*   Dev Shah &emsp;   :`33.33%`
