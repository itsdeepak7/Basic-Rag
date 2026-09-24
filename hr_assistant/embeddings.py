"""step 3 : turn text into numbers (vectors) using JINA."""



from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config
from hr_assistant.logger import get_logger

from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__) 

def get_embeddings_model():
    """ returns a jina embedding model.
    reads JINA_API_KEY from its environment.
    """
    logger.info("initialising embeddings model '%s'",config.EMBEDDINGS_MODEL_NAME)
    return JinaEmbeddings(
        model_name=config.EMBEDDINGS_MODEL_NAME)
   
def get_embeddings_model():
    """Returns a Jina embedding model using explicit configuration."""

    api_key = config.JINA_API_KEY
    logger.info("Initializing embeddings model '%s'", config.EMBEDDINGS_MODEL_NAME)
    
    return JinaEmbeddings(
        model_name=config.EMBEDDINGS_MODEL_NAME,
        jina_api_key=api_key,)