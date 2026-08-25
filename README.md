# HR Policy Assistant (RAG)

A retrieval-augmented generation (RAG) chatbot that answers employee questions about a company's HR policy document. Built with LangChain, Google-hosted LLMs, Jina embeddings, and a FAISS vector store

## How it works

**Ingest** — `hr_assistant/document_loader.py` loads `data/hr_policy.txt`, and `hr_assistant/splitter.py` splits it into chunks (`CHUNK_SIZE=500`, `CHUNK_OVERLAP=60`).

**Embed & store** — `hr_assistant/embeddings.py` creates embeddings with Jina (`jina-embeddings-v2-base-en`), and `hr_assistant/vector_store.py` uploads/loads them from a FAISS collection (reused on subsequent runs instead of re-embedding).

**Retrieve** — `hr_assistant/tools.py` wraps the vector store retriever (top-k = 3) as a `search_hr_policy` tool.

**Agent** — `hr_assistant/agent.py` builds a LangChain agent (`gemini-3.6-flash` via google gemini) that calls the search tool to ground its answers.

Everything is wired together in `hr_assistant/pipeline.py` (`build_hr_assistant()` / `ask()`), used by both entry points below.

## Entry points

`python main.py` — CLI demo that asks a few sample HR questions.

`streamlit run app.py` — interactive chat UI.

`rag.ipynb` — notebook version for experimentation.


## Setup

1. Install [uv]:
pip install uv

2. Create and activate a virtual environment:
uv venv ragenv
ragenv\Scripts\activate

3. Install dependencies:
uv pip install -r requirements.txt

4. Create a `.env` file with:
GROQ_API_KEY=...
JINA_API_KEY=...
GOOGLE_API_KEY=...

## Git basics
git add .
git commit -m "Some message"
git push