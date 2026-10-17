""" ALL  Settings for the app live here ,all in one place"""

import os
from dotenv import load_dotenv

load_dotenv()

##ENV VAR / SECRET
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#GATEWAY
PORTKEY_API_KEY =os.getenv("PORTKEY_API_KEY")
PORTKEY_CONFIG_SLUG = os.getenv("PORTKEY_CONFIG_SLUG")

DATA_FILE_PATH = os.path.join("data","hr_policy.txt")


# TRACING 

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")


#IN MEMORY 
# PERSISTENT MEMORY 
#CLO;UD MEMORY
# VECTOR_STORE_PATH = os.path.join("data","faiss_index")
QDRANT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME","hr_policy")

#MODELS
#LLM AND EMBEDDING MODEL
LLM_MODEL_NAME = "gemini-3.5-flash"
##"openai/gpt-oss-20b"

#GUARD MODEL
GUARD_MODEL_NAME = "openai/gpt-oss-safeguard-20b"

EMBEDDINGS_MODEL_NAME = "jina-embeddings-v2-base-en"

#CHUNK / TEXT SPLITTER CONFIG 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 60

#RETRIEVAL RESULTS
TOP_K_RESULTS =  3

SYSTEM_PROMPT = (
    "You are a friendly HR  assistant. Always use the search_hr_policy tool to look up"
    "facts before answering .If the naswer isnt in the search results,say you dont know "
    "Instead of guessing."
)

def check_api_keys()->None:
    """stop early with a clear messages if a required API key is missing ."""
    if not GROQ_API_KEY:
        raise ValueError("missing GROQ_API_KEY. please add it to your .env file.")
    if not JINA_API_KEY:
        raise ValueError("missing JINA_API_KEY. please add it your .env file.")
    