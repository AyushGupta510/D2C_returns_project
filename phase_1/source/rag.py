
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

import streamlit as st

from config import GROQ_API_KEY

# Use the Groq model that worked in your notebook.
GROQ_MODEL = "openai/gpt-oss-120b"


# Find the policy file relative to this Python module,
# not relative to the terminal's current directory.
# Locate the phase_1 directory relative to this file.
SOURCE_DIR = Path(__file__).resolve().parent
PHASE_DIR = SOURCE_DIR.parent

# Build the absolute path to the policy document.
POLICY_PATH = PHASE_DIR / "documents" / "return_policy.txt"

# Reuse the FAISS index across Streamlit reruns instead of rebuilding it.
@st.cache_resource
def build_policy_retriever():

    # Stop early with a clear message if the policy file is missing.
    if not POLICY_PATH.exists():
        raise FileNotFoundError(
            f"Return policy not found: {POLICY_PATH}"
        )

    # Load the policy as documents for retrieval.
    documents = TextLoader(
        str(POLICY_PATH),
        encoding="utf-8"
    ).load()

    # Split the policy into overlapping chunks so relevant
    # information can be retrieved in manageable passages.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(documents)

    # Use the same embedding model as the notebook prototype.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    # Create a searchable vector index from the policy chunks.
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Return a retriever that supplies the three most relevant chunks.
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


def answer_policy_question(question: str) -> str:
    """Answer a question using retrieved policy evidence."""

    # Reject blank questions before invoking the model.
    if not question or not question.strip():
        raise ValueError("The policy question cannot be empty.")

    # Build the policy index and retrieve relevant evidence.
    retriever = build_policy_retriever()
    documents = retriever.invoke(question)

    # Keep the source passages visible to the language model.
    evidence = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"Passage: {doc.page_content}"
        for doc in documents
    )

    # Initialize the configured Groq model.
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0
    )

    # Instruct the model to use evidence rather than invent policy.
    prompt = f"""
You answer questions about the supplied return-policy evidence.

Rules:
- Answer only from the evidence provided.
- Do not invent policy rules or details.
- If the evidence does not answer the question, say so.
- Distinguish policy statements from recommendations.

Question:
{question}

Retrieved policy evidence:
{evidence}

Answer with a concise explanation and identify the evidence used.
"""

    response = llm.invoke(prompt)
    return response.content
