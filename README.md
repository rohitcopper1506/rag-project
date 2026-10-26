# RAG Knowledge Assistant

A clean, portfolio-ready **Retrieval-Augmented Generation (RAG)** project built with Python, Streamlit, Sentence Transformers, FAISS, and Ollama.

The application lets you upload documents, builds a searchable vector index, retrieves the most relevant chunks for a question, and asks an LLM to answer using those retrieved chunks.

## Features

- Upload PDF, DOCX, and TXT documents
- Automatic text extraction
- Configurable chunk size and overlap
- Semantic embeddings using Sentence Transformers
- Fast vector similarity search with FAISS
- Top-k relevant chunk retrieval
- Local LLM generation through Ollama
- Answers grounded in retrieved document context
- Displays retrieved sources and similarity scores
- Persistent FAISS index and metadata
- Streamlit web interface
- Unit tests for chunking and retrieval
- No documents or API keys committed to Git

## Architecture

```text
                 ┌─────────────────────┐
                 │   PDF / DOCX / TXT  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Text Extraction   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Chunking + Metadata │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Sentence Embeddings │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     FAISS Index     │
                 └──────────┬──────────┘
                            │
               User Question
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Question Embedding  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Top-K Retrieval     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Prompt + Context  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Ollama Local LLM    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Grounded Answer     │
                 └─────────────────────┘
```

## Tech Stack

- **Python**
- **Streamlit** — web UI
- **FAISS** — vector similarity search
- **Sentence Transformers** — text embeddings
- **Ollama** — local LLM inference
- **PyPDF** — PDF extraction
- **python-docx** — DOCX extraction

## Project Structure

```text
rag-project/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm.py
│   └── rag_pipeline.py
├── tests/
│   ├── __init__.py
│   ├── test_chunker.py
│   └── test_retriever.py
├── data/
│   └── README.md
└── storage/
    └── .gitkeep
```

## 1. Requirements

Install Python 3.10+.

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Install Ollama

Install Ollama from its official website and then pull a model.

Example:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before asking questions.

The default model in this project is:

```text
llama3.2:3b
```

You can change it with the `OLLAMA_MODEL` environment variable.

## 3. Run the Application

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## 4. Using the App

1. Upload one or more PDF/DOCX/TXT files.
2. Choose the chunk size and overlap.
3. Click **Build / Update Index**.
4. Enter a question.
5. The system retrieves the most relevant chunks.
6. The LLM generates an answer using only the retrieved context.
7. Expand **Retrieved Sources** to inspect the evidence.

## Environment Variables

Copy `.env.example` to `.env` if you want custom settings.

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=5
```

## How RAG Works

### 1. Ingestion

Documents are converted into plain text.

### 2. Chunking

Large documents are divided into smaller overlapping chunks.

For example:

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

Overlap prevents important information from being lost at chunk boundaries.

### 3. Embedding

Each chunk is converted into a numerical vector using a Sentence Transformer.

```text
"Operating systems manage processes"
                 ↓
[0.12, -0.44, 0.81, ...]
```

### 4. Indexing

The vectors are stored in FAISS for efficient similarity search.

### 5. Retrieval

The user's question is embedded and compared with stored vectors.

The highest-scoring chunks are selected.

### 6. Generation

The retrieved chunks are inserted into a prompt:

```text
Context:
<retrieved chunks>

Question:
<user question>

Answer:
```

The local LLM generates the final answer.

## Why RAG Instead of Fine-Tuning?

Fine-tuning changes model behavior/weights. RAG keeps the model separate from the knowledge base.

RAG is useful when:

- Documents change frequently
- You need answers from private documents
- You want source evidence
- You do not want to retrain a model
- You need a relatively simple knowledge-base update process

## Limitations

This is an educational/portfolio RAG system. Production systems would normally add:

- Better PDF parsing and OCR
- Hybrid keyword + vector search
- Re-ranking
- Query rewriting
- Citation verification
- Access control
- Document versioning
- Evaluation datasets
- Observability and tracing
- Background ingestion jobs
- Database-backed metadata
- Authentication
- Rate limiting

## Running Tests

```bash
pytest
```

## GitHub

Before pushing:

```bash
git init
git add .
git commit -m "Initial RAG project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do **not** commit `.env`, private documents, or generated vector indexes.

## Resume Description

> Built a Retrieval-Augmented Generation (RAG) knowledge assistant using Python, Streamlit, Sentence Transformers, FAISS, and Ollama. Implemented document ingestion, semantic chunking, vector indexing, top-k retrieval, and context-grounded LLM responses with inspectable source chunks.

## License

MIT License.
