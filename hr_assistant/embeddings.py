"""step 3 : turn text into numbers (vectors) using JINA."""



from langchain_community.embeddings import JinaEmbeddings
from hr_assistant import config 

from dotenv import load_dotenv

load_dotenv()
def get_embeddings_model():
    """ returns a jina embedding model.
    reads JINA_API_KEY from its environment.
    """
    return JinaEmbeddings(model_name = config.EMBEDDINGS_MODEL_NAME,)