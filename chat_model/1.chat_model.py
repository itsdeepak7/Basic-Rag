from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = "llama-3.1-8b-instant"

llm = ChatGroq(model=model)


result = llm.invoke("what is the capital of India")

print(result.content)
