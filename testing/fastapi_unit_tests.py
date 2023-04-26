from _fastapi.embeddings import generate_embedding
from _fastapi.main import preprocess_and_chunk as mpc
from _fastapi.pinecone_utils import PineconeUtils
from _fastapi.preprocessor import preprocess_and_chunk as ppc
from _fastapi.text_extractor import extract_text_from_file
import pinecone

def test_generate_embedding():
    # Test inputs
    chunks = ['This is the first sentence.', 'This is the second sentence.']
    file_name = 'test.txt'

    # Expected output
    expected_output = {'vectors': [{'id': 'vec_1234567890_0', 
                                    'values': [-0.3295359010696411, ..., -0.06757882267284393], 
                                    'metadata': {'chunk': 'This is the first sentence.', 'file_name': 'test.txt'}},
                                   {'id': 'vec_1234567890_1', 
                                    'values': [-0.3147587471008301, ..., -0.09722548794746399], 
                                    'metadata': {'chunk': 'This is the second sentence.', 'file_name': 'test.txt'}}]}

    # Generate actual output
    actual_output = generate_embedding(chunks, file_name)

    # Test that the actual output matches the expected output
    assert actual_output == expected_output


import requests

def test_upsert():
    url = "http://localhost:8000/upsert/"
    input_str = "This is a sample input string."
    filename = "sample_file.txt"
    payload = {"input_str": input_str, "filename": filename}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "vectors" in response.json()
    assert isinstance(response.json()["vectors"], list)
    assert len(response.json()["vectors"]) == len(mpc(input_str))
    # Add more assertions as needed


import unittest

class TestPineconeUtils(unittest.TestCase):

    def test_get_index_list(self):
        # Create PineconeUtils object
        pinecone_utils = PineconeUtils(api_key="API_KEY", environment="ENVIRONMENT")
        # Call the function and assert that it returns a list
        self.assertIsInstance(pinecone_utils.get_index_list(), list)

    def test_create_embeddings(self):
        # Create PineconeUtils object
        pinecone_utils = PineconeUtils(api_key="API_KEY", environment="ENVIRONMENT")
        # Call the function with some sample text and assert that it returns a list
        self.assertIsInstance(pinecone_utils.create_embeddings(texts=["hello world"], embed_model="text-davinci-002"), list)

    def test_initialize_index(self):
        # Create PineconeUtils object
        pinecone_utils = PineconeUtils(api_key="API_KEY", environment="ENVIRONMENT")
        # Call the function with some sample arguments and assert that it returns a Pinecone index object
        self.assertIsInstance(pinecone_utils.initialize_index(index_name="test_index", dimensions=10), pinecone.Index)

    def test_create_vector_object(self):
        # Create PineconeUtils object
        pinecone_utils = PineconeUtils(api_key="API_KEY", environment="ENVIRONMENT")
        # Call the function with some sample arguments and assert that it returns a dictionary
        self.assertIsInstance(pinecone_utils.create_vector_object(id="test_id", values=[1.0, 2.0, 3.0]), dict)

    def test_upsert_vectors(self):
        # Create PineconeUtils object
        pinecone_utils = PineconeUtils(api_key="API_KEY", environment="ENVIRONMENT")
        # Call the function with some sample vectors and assert that it returns a dictionary
        vectors = [
            pinecone_utils.create_vector_object(id="test_id1", values=[1.0, 2.0, 3.0]),
            pinecone_utils.create_vector_object(id="test_id2", values=[4.0, 5.0, 6.0]),
            pinecone_utils.create_vector_object(id="test_id3", values=[7.0, 8.0, 9.0])
        ]
        self.assertIsInstance(pinecone_utils.upsert_vectors(vectors=vectors, index_name="test_index"), dict)



def test_preprocess_and_chunk():
    text = "John visited New York City last week. He loved the Statue of Liberty and the Empire State Building."
    expected_output = ['John', 'New York City', 'week', 'Statue', 'Liberty', 'Empire State Building']
    assert ppc(text) == expected_output

    text = "The quick brown fox jumped over the lazy dog."
    expected_output = ['quick brown fox', 'lazy dog']
    assert ppc(text) == expected_output

    text = "My favorite color is blue."
    expected_output = ['favorite color', 'blue']
    assert ppc(text) == expected_output



def test_extract_text_from_file():
    # Test extracting text from a .txt file
    txt_file_path = 'test_files/test.txt'
    expected_txt = 'This is a test file for unit testing.'
    assert extract_text_from_file(txt_file_path) == expected_txt

    # Test extracting text from a .csv file
    csv_file_path = 'test_files/test.csv'
    expected_csv = 'Name, Age\nJohn, 25\nJane, 30\n'
    assert extract_text_from_file(csv_file_path) == expected_csv

    # Test extracting text from a .pdf file
    pdf_file_path = 'test_files/test.pdf'
    expected_pdf = 'This is a test PDF file for unit testing.'
    assert extract_text_from_file(pdf_file_path) == expected_pdf

    # Test extracting text from a .json file
    json_file_path = 'test_files/test.json'
    expected_json = '{"name": "John", "age": 25}'
    assert extract_text_from_file(json_file_path) == expected_json

    # Test extracting text from an .html file
    html_file_path = 'test_files/test.html'
    expected_html = 'This is a test HTML file for unit testing.'
    assert extract_text_from_file(html_file_path) == expected_html

    # Test extracting text from a file with an unsupported format
    unsupported_file_path = 'test_files/test.xlsx'
    try:
        extract_text_from_file(unsupported_file_path)
    except ValueError as e:
        assert str(e) == "File format '.xlsx' is not supported."




if __name__ == "__main__":
    test_generate_embedding()
    test_upsert()
    test_preprocess_and_chunk()
    test_extract_text_from_file()
    print("All test cases passed!")