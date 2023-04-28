from decouple import config
import openai
from pinecone_utils import PineconeUtils
from embeddings import generate_embedding, mpnet_embeddings

pinecone_utils = PineconeUtils(config("PINECONE_API_KEY"), config("PINECONE_ENV"))


def create_prompt(text):
    context = """
    \n The above is a list of some recent positive and negative tweets regarding the company shein,
    analyze the tweets and generate a Brand Image Management report which states a brand image score out of 100 the things customers like,
    major problems faced by customers and also suggest remedies for the same in markdown format
    
    """
    prompt = str(text) + context

    return prompt


def generate_response(prompt):
    openai.api_key = config("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message
    return response["content"]


def generative_search(query):
    query_embeds = mpnet_embeddings(query)
    vec_search = pinecone_utils.search_index("sutra-ai", 10, query_embeds.tolist())
    rel_chunk = [x['metadata']['chunk'] for x in vec_search['matches']]
    prompt = f"{rel_chunk}" + f"\nbased on the context above answer the following {query}"
    response = generate_response(prompt)
    return response

# print(generative_search("This is a good day"))


# create_index = pinecone_utils.initialize_index("sutra-ai",768)
# print(create_index)
