from decouple import config
import openai

# get API key from top-right dropdown on OpenAI website
openai.api_key =config("OPENAI_API_KEY")




def complete(prompt):
    # query text-davinci-003
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return res['choices'][0]['text'].strip()

# query = (
#     "Which training method should I use for sentence transformers when " +
#     "I only have pairs of related sentences?"
# )

# print(complete(query))



embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=embed_model
)

# print(res,len(res['data']))
# print(len(res['data'][0]['embedding']), len(res['data'][1]['embedding']))

import openai
import time

def create_embeddings(texts, embed_model):
    """
    Create embeddings for given texts using OpenAI's GPT-3 model.

    Args:
        texts (list): List of texts for which embeddings need to be created.
        embed_model (str): Engine name for embedding model, e.g. "text-davinci-002".

    Returns:
        list: List of embeddings for the given texts.
    """
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


# embeds = create_embeddings(["Sample document text goes here","there will be several phrases in each batch"],"text-embedding-ada-002")
# print(len(embeds))

def create_vector(id, values, sparse_values=None, metadata=None):
    """
    Creates an object for upserting vectors.

    Args:
        id (str): The vector's unique id.
        values (list of floats): The vector data.
        namespace (str): The namespace name where you upsert vectors.
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


def upsert_vectors(api_key, environment, vectors, index_name):
    """
    Upsert vectors with metadata and sparse values to a Pinecone index.

    Args:
        api_key (str): API key for Pinecone.
        environment (str): Pinecone environment.
        vectors (list): List of dictionaries representing vectors with associated metadata and sparse values.
        namespace (str): Namespace for the Pinecone index.

    Returns:
        dict: Response from Pinecone index upsert operation.
    """
    pinecone.init(api_key=api_key, environment=environment)
    index = pinecone.Index(index_name)
    upsert_response = index.upsert(vectors=vectors)
    return upsert_response

vectors=[
        {
        'id':'vec1', 
        'values':[0.1, 0.2, 0.3, 0.4], 
        'metadata':{'genre': 'drama'},
           'sparse_values':
           {'indices': [10, 45, 16],
           'values':  [0.5, 0.5, 0.2]}},
        {'id':'vec2', 
        'values':[0.2, 0.3, 0.4, 0.5], 
        'metadata':{'genre': 'action'},
           'sparse_values':
           {'indices': [15, 40, 11],
           'values':  [0.4, 0.5, 0.2]}}
    ]
print(upsert_vectors("09890b7f-3119-4d98-924b-bb2ded7b9b52","us-west4-gcp",vectors,"new-data"))

