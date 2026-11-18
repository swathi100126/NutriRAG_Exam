import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def resolve_groq_api_key():
    """Read the Groq key from the environment, then from Streamlit secrets."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        import streamlit as st

        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None

DOCUMENTS_PATH = "documents"
CHROMA_PATH = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"