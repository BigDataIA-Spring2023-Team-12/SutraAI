import os
import docx2txt
import PyPDF2
from bs4 import BeautifulSoup
import io
import json
import csv
from pdfminer.high_level import extract_text as pdf_extract_text

def extract_text_from_file(file_path):
    """
    This function takes a file path as input, recognizes the file format, and extracts the text from the file.

    Args:
        file_path (str): The path of the file to be processed.

    Returns:
        str: The text extracted from the file.
    """

    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == '.docx':
        text = docx2txt.process(file_path)
    elif file_ext == '.pdf':
        with open(file_path, 'rb') as f:
            text = pdf_extract_text(f)
    elif file_ext == '.txt':
        with open(file_path, 'r') as f:
            text = f.read()
    elif file_ext == '.html' or file_ext == '.xml' or file_ext == '.json' or file_ext == '.csv':
        with open(file_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            text = soup.get_text()
    else:
        raise ValueError('Invalid file format')

    return text.strip()

