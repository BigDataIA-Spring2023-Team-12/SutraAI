import time
import pinecone
import openai 
from decouple import config
from vector_search_engine.pinecone_utils import PineconeUtils


# pinecone_utils = PineconeUtils(config("PINECONE_API_KEY"),config("PINECONE_ENV"))


# print(pinecone_utils.initialize_index("chhavi-ai",512))
