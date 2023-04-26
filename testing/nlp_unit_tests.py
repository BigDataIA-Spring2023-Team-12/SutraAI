from nlp.embeddings import generate_embedding
from nlp.preprocessor import preprocess_and_chunk
from nlp.text_extractor import extract_text_from_file



def test_generate_embedding():
    chunks = ["Create Pinecone format dictionary", "get current timestamp and convert"]
    file_name = "hello.py"
    result = generate_embedding(chunks, file_name)
    assert isinstance(result, dict)
    assert len(result["vectors"]) == len(chunks)
    assert isinstance(result["vectors"][0]["id"], str)
    assert isinstance(result["vectors"][0]["values"], list)
    assert isinstance(result["vectors"][0]["metadata"], dict)
    assert result["vectors"][0]["metadata"]["chunk"] == chunks[0]
    assert result["vectors"][0]["metadata"]["file_name"] == file_name
    assert isinstance(result["vectors"][1]["id"], str)
    assert isinstance(result["vectors"][1]["values"], list)
    assert isinstance(result["vectors"][1]["metadata"], dict)
    assert result["vectors"][1]["metadata"]["chunk"] == chunks[1]
    assert result["vectors"][1]["metadata"]["file_name"] == file_name


def test_preprocess_and_chunk():
    text = "The quick brown fox jumps over the lazy dog. John Smith is a software engineer at Google."
    expected_output = ['quick brown fox', 'lazy dog', 'John Smith', 'software engineer', 'Google']
    assert preprocess_and_chunk(text) == expected_output


def test_extract_text_from_file():
    # Test for a PDF file
    pdf_file_path = 'test_files/sample.pdf'
    extracted_text = extract_text_from_file(pdf_file_path)
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

    # Test for a JSON file
    json_file_path = 'test_files/sample.json'
    extracted_text = extract_text_from_file(json_file_path)
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

    # Test for a text file
    txt_file_path = 'test_files/sample.txt'
    extracted_text = extract_text_from_file(txt_file_path)
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

    # Test for an HTML file
    html_file_path = 'test_files/sample.html'
    extracted_text = extract_text_from_file(html_file_path)
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

    # Test for an unsupported file format
    unsupported_file_path = 'test_files/sample.jpg'
    try:
        extracted_text = extract_text_from_file(unsupported_file_path)
    except ValueError as e:
        assert str(e) == "File format '.jpg' is not supported."


if __name__ == "__main__":
    test_generate_embedding()
    test_preprocess_and_chunk()
    test_extract_text_from_file()
    print("All test cases passed!")