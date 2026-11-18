from pathlib import Path

import chromadb
from pypdf import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer

from config import (
    DOCUMENTS_PATH,
    CHROMA_PATH,
    EMBEDDING_MODEL
)
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="nutrition_documents"
)
def load_document(file_path):

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif file_path.endswith(".docx"):
        document = Document(file_path)
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""
def split_text(text, chunk_size=500, overlap=50):

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
def get_all_documents():
    all_texts = []
    for file_path in Path(DOCUMENTS_PATH).iterdir():
        if file_path.suffix.lower() in [".pdf", ".docx"]:
            text = load_document(str(file_path))
            if text.strip():
                all_texts.append({
                    "text": text,
                    "source": file_path.name
                })
    return all_texts

def create_embeddings(chunks):

    embeddings = embedding_model.encode(chunks)

    return embeddings.tolist()
def store_in_chromadb(chunks, embeddings, source):

    ids = [
        f"{source}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {"source": source}
        for _ in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
def ingest_documents():

    documents = get_all_documents()

    for document in documents:

        text = document["text"]
        source = document["source"]

        chunks = split_text(text)

        embeddings = create_embeddings(chunks)

        store_in_chromadb(chunks, embeddings, source)

        print(f"Processed: {source}")

    print("All documents processed successfully!")
if __name__ == "__main__":
    ingest_documents()


