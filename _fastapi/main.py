from fastapi import FastAPI
from pydantic import BaseModel
from embeddings import generate_embedding
from preprocessor import preprocess_and_chunk
from pinecone_utils import PineconeUtils
from decouple import config
from vector_search import generative_search



# from fastapi_utils.tasks import repeat_every
# @app.on_event("startup")
# @repeat_every(seconds=300)  # 1 hour
# def reset_api_calls() -> None:
#     reset_calls()
    
pinecone_utils = PineconeUtils(config("PINECONE_API_KEY"), config("PINECONE_ENV"))

app = FastAPI()


class StringInput(BaseModel):
    input_str: str
    filename: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upsert/")
async def upsert(string_input: StringInput):
    """
    A POST endpoint that takes in a string and a file name, and allows for the addition
    of functions to modify the string. Returns the result of the selected function.
    """
    input_str = string_input.input_str
    filename = string_input.filename
    print("error here")
    chunk_list = preprocess_and_chunk(input_str)
    vectors = generate_embedding(chunk_list, filename)  # Replace with function of your choice
    
    upsert_res = pinecone_utils.upsert_vectors(vectors, "sutra-ai")

    # Return the modified string as the API response
    return {"upserted_count:":f"{upsert_res}"}

@app.get("/vec-search/{query}")
async def vec_search(query):
    """
   
    """
    response = generative_search(query)

    # Return the modified string as the API response
    return {"response":response}
