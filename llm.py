from groq import Groq

from config import GROQ_API_KEY
client = Groq(
    api_key=GROQ_API_KEY
)
def generate_response(prompt):

    response = client.chat.completions.create(
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