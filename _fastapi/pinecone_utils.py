import time
import pinecone
import openai 
from decouple import config


class PineconeUtils:
    def __init__(self, api_key, environment):
        self.api_key = api_key
        self.environment = environment

    def get_index_list(self):
        # Initialize connection to Pinecone
        pinecone.init(api_key=self.api_key, environment=self.environment)
        return pinecone.list_indexes()

    def create_embeddings(self, texts, embed_model):
        """
        Create embeddings for given texts using OpenAI's GPT-3 model.

        Args:
            texts (list): List of texts for which embeddings need to be created.
            embed_model (str): Engine name for embedding model, e.g. "text-davinci-002".

        Returns:
            list: List of embeddings for the given texts.
        """
        openai.api_key =config("OPENAI_API_KEY")
        try:
            res = openai.Embedding.create(input=texts, engine=embed_model)
        except openai.error.RateLimitError:
            done = False
            while not done:
                time.sleep(5)
                try:
                    res = openai.Embedding.create(input=texts, engine=embed_model)
                    done = True
                except openai.error.RateLimitError:
                    pass
        embeds = [record['embedding'] for record in res['data']]
        return embeds

    def initialize_index(self, index_name, dimensions, meta_data_config=None, similarity_metric="cosine", pods=1, replicas=1, pod_type='p1.x1'):
        """
        Initialize connection to Pinecone and create an index if it doesn't exist.

        Args:
            index_name (str): Name of the index to be created.
            dimensions (int): Dimensionality of the vectors.
            meta_data_config (dict): Metadata configuration for the index.
            similarity_metric (str, optional): Similarity metric to be used. Default is "cosine".
            pods (int, optional): Number of pods. Default is 1.
            replicas (int, optional): Number of replicas. Default is 1.
            pod_type (str, optional): Type of pod. Default is 'p1.x1'.

        Returns:
            pinecone.Index: The Pinecone index object.
        """
        # Initialize connection to Pinecone
        pinecone.init(api_key=self.api_key, environment=self.environment)

        # Check if index already exists
        if index_name not in pinecone.list_indexes():
            # If does not exist, create index
            pinecone.create_index(
                name=index_name,
                dimension=dimensions,
                metric=similarity_metric,
                metadata_config=meta_data_config,
                pods=pods,
                replicas=replicas,
                pod_type=pod_type
            )

        # Connect to index
        index = pinecone.Index(index_name)
        # Return the Pinecone index object
        return index

    def create_vector_object(self, id, values, sparse_values=None, metadata=None):
        """
        Creates an object for upserting vectors.

        Args:
            id (str): The vector's unique id.
            values (list of floats): The vector data.
            sparse_values (dict, optional): Vector sparse data represented as a dictionary
            with 'indices' and 'values' keys. Default is None.
            metadata (dict, optional): Metadata included in the request. Default is None.

        Returns:
            dict: The object for upserting vectors.
        """

        vector_object = {
            'id': id,
            'values': values
        }

        if sparse_values is not None:
            vector_object['sparseValues'] = sparse_values

        if metadata is not None:
            vector_object['metadata'] = metadata

        return vector_object

        
    def upsert_vectors(self, vectors, index_name):
        """
        Upsert vectors with metadata and sparse values to a Pinecone index.

        Args:
            vectors (list): List of dictionaries representing vectors with associated metadata and sparse values.
            index_name (str): Namespace for the Pinecone index.

        Returns:
            dict: Response from Pinecone index upsert operation.
            
        """
        pinecone.init(api_key=self.api_key, environment=self.environment)
        index = pinecone.Index(index_name)
        upsert_response = index.upsert(vectors=vectors)
        return upsert_response['upserted_count']
    
    def search_index(self, index_name,topk, vector, meta_filter=None):
        pinecone.init(api_key=self.api_key, environment=self.environment)
        index = pinecone.Index(index_name)
        query_response = index.query(
            top_k=topk,
            include_values=False,
            include_metadata=True,
            vector=vector,
            filter= meta_filter
        )
        return query_response
