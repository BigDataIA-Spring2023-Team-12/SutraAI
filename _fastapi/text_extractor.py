import os
import json


def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a file and returns it as a string.

    Args:
        file_path (str): The path to the file to extract text from.

    Returns:
        str: The extracted text as a string.

    Raises:
        ValueError: If the file format is not supported.

    """

    # Extract the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Determine the appropriate text extraction method based on the file extension
    if file_extension == '.pdf':
        import PyPDF2
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
    elif file_extension == '.json':
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            text = json.dumps(json_data)
    elif file_extension in ['.csv', '.txt', '.doc', '.odt']:
        with open(file_path, 'r') as file:
            text = file.read()
    elif file_extension == '.html':
        from bs4 import BeautifulSoup
        with open(file_path, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            text = soup.get_text()
    else:
        raise ValueError(f"File format '{file_extension}' is not supported.")

    return text