# HR Policy Assistant (RAG)

An enterprise-grade Retrieval-Augmented Generation (RAG) assistant designed to help employees query internal HR policies with precision and confidence. Built with LangChain, Groq-hosted LLMs, Jina AI embeddings, and a Qdrant Cloud vector store, the pipeline integrates dedicated safety guardrails and full LangSmith observability.

---

## Key Features

- **Agentic Retrieval:** Uses a LangChain tool-calling agent to decide when and how to search the policy store before synthesizing answers.
- **Persistent Cloud Vector Store:** Managed on Qdrant Cloud with collection reuse, eliminating redundant re-embedding steps across restarts.
- **Dual-Layer Guardrails:** Independent input screening (prompt injection, cross-employee data requests) and output auditing (PII leakage, unauthorized commitments, malicious links) via a dedicated safety model.
- **End-to-End Tracing:** LangSmith integration for deep visibility into latency, tool invocations, and agent reasoning paths.
- **Multiple Entry Points:** Run via interactive Streamlit Web UI, CLI script, or Jupyter Notebook.

---

## Architecture & How It Works

```text
       [ User Query ]
             │
             ▼
    ┌─────────────────┐
    │ Input Guardrail │ ──► (Blocks prompt injection / data exfiltration)
    └────────┬────────┘
             │ Pass
             ▼
    ┌─────────────────┐       Calls Tool       ┌──────────────────────┐
    │ LangChain Agent │ ─────────────────────► │   search_hr_policy   │
    │ (Groq LLM)      │ ◄───────────────────── │ (Qdrant Cloud, k=3)  │
    └────────┬────────┘       Top-3 Chunks     └──────────────────────┘
             │
             ▼
    ┌──────────────────┐
    │ Output Guardrail │ ──► (Blocks PII leaks / unauthorized promises)
    └────────┬─────────┘
             │ Safe
             ▼
      [ User Answer ]
```

1. **Ingest:** `hr_assistant/document_loader.py` reads `data/hr_policy.txt`, and `hr_assistant/splitter.py` chunks the content with `CHUNK_SIZE=500` and `CHUNK_OVERLAP=60`.
2. **Embed & Store:** `hr_assistant/embeddings.py` generates vectors using `jina-embeddings-v2-base-en`. `hr_assistant/vector_store.py` provisions or reuses existing vectors inside Qdrant Cloud.
3. **Retrieve:** `hr_assistant/tools.py` exposes a vector retriever tool (`top-k = 3`) to search the HR policy.
4. **Agent Inference:** `hr_assistant/agent.py` coordinates the agent (`openai/gpt-oss-20b` hosted on Groq) to invoke retrieval and synthesize grounded responses.
5. **Safety Guardrails:** `hr_assistant/guardrails.py` uses an auxiliary safety model (`openai/gpt-oss-safeguard-20b` on Groq) to evaluate input prompts and filter generated responses.
6. **Unified Pipeline:** `hr_assistant/pipeline.py` provides high-level helpers (`build_hr_assistant()`, `ask()`) invoked across all entry points.

---

## Project Layout

```text
hr_assistant/
├── config.py           # Configuration, environment parsing, and system prompts
├── document_loader.py  # Loads source policy documents
├── splitter.py         # Text chunking logic
├── embeddings.py       # Jina embeddings configuration
├── vector_store.py     # Qdrant Cloud client, collection initialization, and retriever
├── tools.py            # Custom retriever tools exposed to the agent
├── llm.py              # Groq LLM setup
├── agent.py            # LangChain agent workflow definition
├── guardrails.py       # Input/output safety verification
├── pipeline.py         # Main interface connecting components (build_hr_assistant, ask)
├── logger.py           # File logging system (outputting to logs/)
└── tracing.py          # LangSmith configuration and connectivity check

data/
└── hr_policy.txt       # Primary source HR policy document

docs/                   # Technical documentation (logging, LangSmith, migration, security tests)
NOTES/                  # Background research and reference PDFs

main.py                 # CLI demo runner
app.py                  # Streamlit chat interface
rag.ipynb               # Prototyping and experimentation notebook
requirements.txt        # Python package dependencies
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `pip`

### 2. Environment Setup

Clone the repository and prepare your virtual environment:

```bash
# Clone the repository
git clone https://github.com/itsdeepak7/Basic-Rag.git
cd Basic-Rag

# Install uv (if not already installed)
pip install uv

# Create and activate a virtual environment
uv venv ragenv

# Windows:
ragenv\Scripts\activate

# macOS / Linux:
source ragenv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

### 3. Environment Variables Configuration

Create a `.env` file in the root directory:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Jina AI Embeddings
JINA_API_KEY=your_jina_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=hr_policy

# LangSmith Observability (Optional)
LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=hr-policy-assistant
```

---

## Running the Application

### Interactive Web UI (Streamlit)
To launch the chat interface:
```bash
streamlit run app.py
```

### Command-Line Interface (CLI)
To run pre-configured sample questions through the pipeline:
```bash
python main.py
```

### Experimentation Notebook
Launch Jupyter to explore the notebook version:
```bash
jupyter notebook rag.ipynb
```

---

## Safety & Compliance

The assistant enforces zero-trust data constraints across two checkpoints:
- **Input Filtering:** Identifies prompt injection patterns, role-breaking instructions, and requests for unauthorized employee records or compensation data.
- **Output Verification:** Verifies the generated output to block inadvertent disclosures of personally identifiable information (PII), unapproved policy promises, or untrusted URLs.

---

## Git Workflow Reference

Standard commands for pushing ongoing changes:

```bash
git add .
git commit -m "Update HR assistant pipeline"
git push origin main
```