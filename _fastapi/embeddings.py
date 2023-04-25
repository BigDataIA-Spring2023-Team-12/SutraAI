from typing import Dict, Any
import spacy
import time


def generate_embedding(chunks: list, file_name: str) -> Dict[str, Any]:
    """
    Generates embeddings for a list of sentence chunks using the pre-trained spaCy model,
    along with metadata in Pinecone format.

    Args:
    - chunks (list): A list of sentence chunks to generate embeddings for.
    - file_name (str): The name of the file containing the input sentences.

    Returns:
    - pinecone_dict (dict): A dictionary containing the embeddings and metadata in Pinecone format.
    """

    # Load pre-trained spaCy model
    nlp = spacy.load('en_core_web_md')

    # Generate embeddings for each chunk
    vectors = []
    for i, chunk in enumerate(chunks):
        # Get the vector representation for the chunk
        embedding = nlp(chunk).vector

        # Create metadata dictionary
        metadata = {'chunk': chunks[i], 'file_name': file_name}

        # Create Pinecone format dictionary with unique vector ID
        timestamp = str(int(time.time() * 1000))  # get current timestamp and convert to string
        vector_id = 'vec_' + timestamp + '_' + str(i)  # create a unique id using the timestamp and index
        vector = {'id': vector_id, 'values': embedding.tolist(), 'metadata': metadata}
        vectors.append(vector)

    # Combine vectors into Pinecone format dictionary
    pinecone_dict = {'vectors': vectors}
    print(len(pinecone_dict["vectors"][0]["values"]))
    return pinecone_dict
