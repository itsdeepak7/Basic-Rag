""" step 4 : store chunk embeddings in FAISS so we can search them"""

import os
from langchain_community.vectorstores import FAISS
from hr_assistant import config
from hr_assistant.embeddings import get_embeddings_model
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

# build_vector_tore
def build_vector_store(chunks):
    """EMBED every chunk and build 
    a searchable Faiss index in memory. """
    logger.info(
        "Embedding %d chunk(s) and uploading to faiss collection ...",
    )
    embeddings_model = get_embeddings_model()
    vector_store =  FAISS.from_documents(chunks,embeddings_model)
    logger.info("FAISS index build in memory ")
    return vector_store


#save vector_store

def save_vector_store(vector_store,path:str = config.VECTOR_STORE_PATH)->None:
    """SAVE THE FAISS INDEX TO DISK
    SO WE DONT HAVE TO REBUILD IT EVERY TIME."""
    logger.info("saved faiss index to '%s'",path)
    vector_store.save_local(path)

def load_vector_store(path:str = config.VECTOR_STORE_PATH):
    """LOADS A PREVIOUSLY SAVED FAISS INDEX FROM THE DISK."""
    logger.info("loading faiss index from '%s'",path)
    embeddings_model = get_embeddings_model()
    #allow dangerous_deseralisation is  safe here because we only ever load 
    # an index that this same app created and saved .
    return FAISS.load_local(path,embeddings_model,allow_dangerous_deserialization=True)


def vector_store_exists(path:str=config.VECTOR_STORE_PATH )->bool:
    """check if a saved Faiss index already exists on the disk.
    """
    return os.path.exists(os.path.join(path,"index.faiss"))

def get_retriever(vector_store,k:int = config.TOP_K_RESULTS):
    """TURN A VECTOR STPRE INTO A RETRIEVER 
    THAT RETURNS THE TOP-K MACHING CHUNKS."""
    logger.info("Creating retreival with top_k='%d;",k)
    return vector_store.as_retriever(search_kwargs={"k":k})
