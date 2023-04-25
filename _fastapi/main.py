from fastapi import FastAPI
from pydantic import BaseModel
from embeddings import generate_embedding
from preprocessor import preprocess_and_chunk
from pinecone_utils import PineconeUtils
from decouple import config


pinecone_utils = PineconeUtils(config("PINECONE_API_KEY"),config("PINECONE_ENV"))

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

    modified_str = generate_embedding(preprocess_and_chunk(input_str), filename)  # Replace with function of your choice
    upsert_res = pinecone_utils.upsert_vectors(modified_str,"sutra-ai")
    # Return the modified string as the API response
    return {"vectorDB Updated!": upsert_res}

