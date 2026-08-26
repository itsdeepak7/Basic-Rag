"""step 6 : connect to the LLM (the "brain" of the assistant)."""

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from hr_assistant import config 

from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """return a groq chat model. read GROQ_API_KEY FROM THE ENVIRONMENT """
    logger.info("chat model attached '%s'",config.LLM_MODEL_NAME)
    return ChatGoogleGenerativeAI(model = config.LLM_MODEL_NAME)