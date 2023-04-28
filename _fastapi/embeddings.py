from typing import Dict, Any
from sentence_transformers import SentenceTransformer
from decouple import config
from pinecone_utils import PineconeUtils
import time


def generate_embedding(chunks: list, file_name: str) -> Dict[str, Any]:
    """
    Generates embeddings for a list of sentence chunks using the all-mpnet-base-v2 model from SentenceTransformers,
    along with metadata in Pinecone format.

    Args:
    - chunks (list): A list of sentence chunks to generate embeddings for.
    - file_name (str): The name of the file containing the input sentences.

    Returns:
    - pinecone_dict (dict): A dictionary containing the embeddings and metadata in Pinecone format.
    """

    # Load all-mpnet-base-v2 model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Generate embeddings for each chunk
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk, show_progress_bar=True)

        # Create metadata dictionary
        metadata = {'chunk': chunks[i], 'file_name': file_name}

        # Create Pinecone format dictionary with unique vector ID
        timestamp = str(int(time.time() * 1000))  # get current timestamp and convert to string
        vector_id = 'vec_' + timestamp + '_' + str(i)  # create a unique id using the timestamp and index
        vector = {'id': vector_id, 'values': embedding.tolist(), 'metadata': metadata}
        vectors.append(vector)

    return vectors

def mpnet_embeddings(text):
        model = SentenceTransformer('all-mpnet-base-v2')

        embedding = model.encode(text,show_progress_bar=True)

        return embedding
