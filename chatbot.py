from retrieve import retrieve_documents
from llm import generate_response
def ask_question(question):

    results = retrieve_documents(question)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    prompt = f"""
    You are a nutrition and wellness assistant.

    Answer the question using only the context below.
    If the answer is not available in the context,
    say that you don't have enough information.

    Context:
    {context}

    Question:
    {question}
    """

    answer = generate_response(prompt)

    return answer
if __name__ == "__main__":
    question = input("Ask your question: ")
    answer = generate_response(question)
    print("\nAnswer:")
    print(answer)