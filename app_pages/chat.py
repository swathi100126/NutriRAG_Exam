import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.caption("Ask about food, meals, or everyday nutrition. Answers use the saved profile and the local guides.")

profile = st.session_state.get("profile")
if profile:
    allergy_text = ", ".join(profile["allergies"]) if profile["allergies"] else "none reported"
    st.caption(
        f"Using your profile: age {profile['age']}, {profile['goal'].lower()}, "
        f"{profile['diet'].lower()}, allergies {allergy_text}."
    )
else:
    st.info(
        "Save a profile for personalised answers. You can still ask a general question.",
        title="Profile not saved",
    )

if st.button("Clear chat", width="stretch"):
    if st.session_state.messages:
        st.session_state.messages = []
        st.rerun()
    else:
        st.info("The chat is already empty.", title="Nothing to clear")


def _show_message(message):
    st.markdown(message["content"])
    sources = message.get("sources") or []
    if sources:
        st.caption("Sources: " + ", ".join(sources))


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        _show_message(message)

raw_prompt = st.chat_input("Ask a nutrition question", submit_mode="disable")
if raw_prompt is not None and not raw_prompt.strip():
    st.warning("Please enter a question.")
elif raw_prompt:
    prompt = raw_prompt.strip()
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Finding your answer..."):
            try:
                from chatbot import ask_question

                result = ask_question(prompt, st.session_state.get("profile"))
                reply = result["answer"]
                sources = result["sources"]
            except Exception as exc:
                reply = f"I couldn't answer just now. {exc}"
                sources = []
        _show_message({"content": reply, "sources": sources})

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "sources": sources}
    )
