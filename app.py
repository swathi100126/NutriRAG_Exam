import streamlit as st

from safety import DISCLAIMER

st.set_page_config(
    page_title="NutriRAG",
    page_icon=":material/nutrition:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.session_state.setdefault("profile", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("meal_plan", None)

page = st.navigation(
    [
        st.Page("app_pages/profile.py", title="Profile", icon=":material/person:", default=True),
        st.Page("app_pages/chat.py", title="Chat", icon=":material/chat:"),
        st.Page("app_pages/meal_plan.py", title="Meal plan", icon=":material/restaurant:"),
    ],
    position="top",
)

st.title(page.title, icon=page.icon)
st.caption("Nutrition and wellness assistant for everyday eating.")
st.warning(DISCLAIMER, icon=":material/health_and_safety:", title="Nutrition disclaimer")
page.run()
