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

## 👉 Conclusion
The proposed project aims to build a smart query tool that can query multiple documents and retrieve the relevant information based on user input queries. The project will use Google Drive, vector embeddings, indexing, and GPT-3 to achieve this objective. The project will be completed in 2 weeks. The deliverables of the project will be a functional query tool with a user interface. 💻
- `gitignore`: The file containing the list of packages to exclude on git push.
- `_utils.py`: This script fetches text from files in a specific Google Drive folder named 'SutraAI', and sends the text and filename to a FastAPI endpoint for further processing. The script also stores information about the processed files in a SQLite database. The user is required to provide valid credentials for Google Drive API authentication.
- `load_from_drive`: This Python script defines a function named "extract_text_from_file" which takes in a Google Drive file ID and user credentials, and returns the extracted text from the file in string format. It supports various file formats including PDF, JSON, CSV, TXT, DOC, DOCX, ODT, and HTML.
- `main.py`: This Python script uses Streamlit to create a web app that allows users to authenticate with Google Drive and extract text from files, as well as search for information using natural language queries. It uses the Google Drive API and OAuth2 authentication.
- `users.db`: User Logs.