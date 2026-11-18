import streamlit as st

from chatbot import ask_question

st.set_page_config(
    page_title="NutriRAG",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 NutriRAG")
st.subheader("Your AI Nutrition and Wellness Assistant")

st.write(
    "Ask questions about nutrition, healthy eating and wellness."
)
question = st.text_input(
    "Ask your nutrition question:"
)

if st.button("Get Answer"):
    if question:
        with st.spinner("Finding your answer..."):
            answer = ask_question(question)

        st.subheader("NutriRAG Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question.")