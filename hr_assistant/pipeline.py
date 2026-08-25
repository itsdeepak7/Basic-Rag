"""wires all the components together into one ready to use agnets.
This is the single entry point that main.py(CLI) and app.py (stremalit)
both call . Each step is handled by its own small modeule.
"""

from hr_assistant import config

from hr_assistant.agents import create_hr_agent
from hr_assistant.document_loader import load_document
from hr_assistant.llm import get_llm
from hr_assistant.splitter import split_into_chunks
from hr_assistant.tools import create_search_tool
from hr_assistant.vector_stores import (
    build_vector_store,
    get_retriever,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)


def build_vector_store_for_document(file_path: str = config.DATA_FILE_PATH):
    """Load + split + embed the document, 
    reusing saved index if we have one."""
    if vector_store_exists():
        print("Found an existing vector store on disk, connecting to it (fast, no re-embedding).")
        return load_vector_store()

    documents = load_document(file_path)
    chunks = split_into_chunks(documents)
    print(f"Loaded '{file_path}' and split it into {len(chunks)} chunks.")

    vector_store = build_vector_store(chunks)
    save_vector_store(vector_store)
    return vector_store


    
def build_hr_assistant(file_path: str = config.DATA_FILE_PATH):
    """Build the full RAG agent, ready to answer questions."""
    config.check_api_keys()

    vector_store = build_vector_store_for_document(file_path)
    retriever = get_retriever(vector_store)
    search_tool = create_search_tool(retriever)

    llm = get_llm()
    agent = create_hr_agent(llm, [search_tool])

    return agent


def ask(agent, question: str) -> str:
    """Ask the agent a question and
    return its final answer as plain text."""
   
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})

    final_msg = response["messages"][-1]

    if isinstance(final_msg.content,list):
        return final_msg.content[0]["text"]
    
    return final_msg.content

