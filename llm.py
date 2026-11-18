from groq import Groq

from config import resolve_groq_api_key

_client = None


def generate_response(prompt):
    global _client

    api_key = resolve_groq_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file or to Streamlit secrets."
        )

    if _client is None:
        _client = Groq(api_key=api_key)

    response = _client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Ask your question: ")
    answer = generate_response(question)
    print("\nAnswer:")
    print(answer)
