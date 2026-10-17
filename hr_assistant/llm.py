"""step 6 : connect to the LLM (the "brain" of the assistant)."""

from hr_assistant.gateway import get_gateway_llm,get_judge_llm


from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """return a groq chat model. read GROQ_API_KEY FROM THE ENVIRONMENT """
    logger.info("INITIALIZING LLM via portkey")
    return get_gateway_llm()

def get_the_judge_llm():
    """return a groq chat model. read GROQ_API_KEY FROM THE ENVIRONMENT """
    logger.info("INITIALIZING JUDGE LLM via portkey")
    return get_judge_llm()