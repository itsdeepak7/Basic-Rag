""" step 4 : store chunk embeddings in FAISS so we can search them"""

import os
from langchain_community.vectorstores import FAISS
from hr_assistant import config
from hr_assistant.embeddings import get_embeddings_model

# build_vector_tore
def build_vector_store(chunks):
    """EMBED every chunk and build 
    a searchable Faiss index in memory. """
    embeddings_model = get_embeddings_model()
    return FAISS.from_documents(chunks,embeddings_model)


#save vector_store

def save_vector_store(vector_store,path:str = config.VECTOR_STORE_PATH)->None:
    """SAVE THE FAISS INDEX TO DISK
    SO WE DONT HAVE TO REBUILD IT EVERY TIME."""
    vector_store.save_local(path)

def load_vector_store(path:str = config.VECTOR_STORE_PATH):
    """LOADS A PREVIOUSLY SAVED FAISS INDEX FROM THE DISK."""
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
    return vector_store.as_retriever(search_kwargs={"k":k})
