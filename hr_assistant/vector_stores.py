""" step 4 : store chunk embeddings in QDRANT CLOUD so we can search them"""

import os
#from langchain_community.vectorstores import FAISS
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from hr_assistant import config
from hr_assistant.embeddings import get_embeddings_model

from hr_assistant.logger import get_logger

logger = get_logger(__name__)

# build_vector_tore
def build_vector_store(chunks):
    """Embed every chunk and upload it into a Qdrant Cloud collection."""
    logger.info(
        "Embedding %d chunk(s) and uploading to Qdrant collection '%s'...",
        len(chunks),
        config.QDRANT_COLLECTION_NAME,
    )
    embeddings_model = get_embeddings_model()
    vector_store = QdrantVectorStore.from_documents(
        chunks,
        embedding=embeddings_model,
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        collection_name=config.QDRANT_COLLECTION_NAME,
    )
    logger.info("Uploaded to Qdrant collection '%s'", config.QDRANT_COLLECTION_NAME)
    return vector_store

#save vector_store

# def save_vector_store(vector_store,path:str = config.VECTOR_STORE_PATH)->None:
#     """SAVE THE FAISS INDEX TO DISK
#     SO WE DONT HAVE TO REBUILD IT EVERY TIME."""
#     logger.info("saved faiss index to '%s'",path)
#     vector_store.save_local(path)


def load_vector_store():
    """Connect to a Qdrant Cloud collection that was already built before."""
    logger.info("Connecting to existing Qdrant collection '%s'", config.QDRANT_COLLECTION_NAME)
    embeddings_model = get_embeddings_model()
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings_model,
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
        collection_name=config.QDRANT_COLLECTION_NAME,
    )
# def vector_store_exists(path:str=config.VECTOR_STORE_PATH )->bool:
#     """check if a saved Faiss index already exists on the disk.
#     """
#     return os.path.exists(os.path.join(path,"index.faiss"))


def vector_store_exists() -> bool:
    """Check if the Qdrant Cloud collection already exists."""
    client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
    return client.collection_exists(config.QDRANT_COLLECTION_NAME)




def get_retriever(vector_store, k: int = config.TOP_K_RESULTS):
    """Turn a vector store into a retriever
    that returns the top-k matching chunks."""
    logger.info("Creating retriever with top_k=%d", k)
    return vector_store.as_retriever(search_kwargs={"k": k})