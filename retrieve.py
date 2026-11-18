import chromadb
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_PATH,
    EMBEDDING_MODEL
)
embedding_model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name="nutrition_documents"
)
def retrieve_documents(question):

    question_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    return results
if __name__ == "__main__":
    question = "What are good vegetarian protein sources?"

    results = retrieve_documents(question)

    for document in results["documents"][0]:
        print(document)
        print("--------------------")