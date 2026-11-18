from safety import assess_question


def _display_source(name):
    cleaned = name.lstrip("#- ").strip()
    return cleaned or name


def _profile_text(profile):
    if not profile:
        return "No personal profile was saved."
    allergies = profile.get("allergies") or []
    allergy_text = ", ".join(allergies) if allergies else "none reported"
    return (
        f"Age {profile['age']}, goal {profile['goal']}, diet {profile['diet']}, "
        f"allergies {allergy_text}."
    )


def ask_question(question, profile=None):
    decision = assess_question(question)
    if decision.refused:
        return {
            "answer": decision.message,
            "sources": [],
            "refused": True,
        }

    from retrieve import retrieve_documents

    results = retrieve_documents(question)
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]

    labelled_chunks = []
    sources = []
    for document, metadata in zip(documents, metadatas):
        source = _display_source((metadata or {}).get("source") or "unknown")
        if source not in sources:
            sources.append(source)
        labelled_chunks.append(f"Source: {source}\n{document}")

    context = "\n\n".join(labelled_chunks) if labelled_chunks else "No matching passages were found."

    prompt = f"""
    You are a nutrition and wellness assistant.

    Use the personal profile only to tailor food suggestions.
    Answer the question using only the context below.
    If the answer is not available in the context,
    say that you don't have enough information.
    Do not diagnose, prescribe, or recommend medicines.
    Mention the source file names you used.

    Profile:
    {_profile_text(profile)}

    Context:
    {context}

    Question:
    {question}
    """

    from llm import generate_response

    answer = generate_response(prompt)
    return {
        "answer": answer,
        "sources": sources,
        "refused": False,
    }


if __name__ == "__main__":
    question = input("Ask your question: ")
    result = ask_question(question)
    print("\nAnswer:")
    print(result["answer"])
    if result["sources"]:
        print("\nSources:")
        print(", ".join(result["sources"]))
