import streamlit as st

from src.config import settings
from src.document_loader import load_uploaded_documents
from src.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 RAG Knowledge Assistant")
st.caption("Ask questions about your own PDF, DOCX, and TXT documents.")

@st.cache_resource
def get_pipeline():
    return RAGPipeline(settings)


pipeline = get_pipeline()

with st.sidebar:
    st.header("Configuration")
    chunk_size = st.slider("Chunk size", 300, 2000, 800, step=100)
    overlap = st.slider("Chunk overlap", 0, 400, 120, step=20)
    top_k = st.slider("Top-K retrieved chunks", 1, 10, settings.top_k)

    st.divider()
    st.write(f"**Embedding:** `{settings.embedding_model}`")
    st.write(f"**LLM:** `{settings.ollama_model}`")

uploaded_files = st.file_uploader(
    "Upload knowledge-base documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    if st.button("🔨 Build / Update Index", type="primary"):
        with st.spinner("Reading documents, creating embeddings, and building the index..."):
            documents = load_uploaded_documents(uploaded_files)
            count = pipeline.build_index(
                documents,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        st.success(f"Indexed {count} chunks from {len(uploaded_files)} document(s).")

if pipeline.has_index():
    st.success("Vector index is ready.")
else:
    st.info("Upload documents and build an index to start asking questions.")

question = st.text_input(
    "Ask a question",
    placeholder="e.g. What are the main conclusions of the document?",
)

if st.button("🔎 Ask", disabled=not pipeline.has_index() or not question.strip()):
    with st.spinner("Retrieving context and generating answer..."):
        result = pipeline.answer(question, top_k=top_k)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Retrieved Sources")
    for i, item in enumerate(result["sources"], start=1):
        with st.expander(
            f"Source {i}: {item['source']} | score={item['score']:.4f}"
        ):
            st.write(item["text"])
