import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foods import ALLERGY_OPTIONS, DIETS, GOALS, validate_profile

st.caption(
    "Vegetarian includes dairy and excludes eggs, meat, and fish. "
    "Vegan excludes all animal foods. Eggetarian adds eggs."
)

saved = st.session_state.get("profile") or {}

with st.form("profile_form"):
    age = st.number_input(
        "Age",
        min_value=16,
        max_value=80,
        value=int(saved.get("age", 25)),
        step=1,
        help="Ages 16 to 80.",
    )
    goal = st.segmented_control(
        "Health goal",
        GOALS,
        default=saved.get("goal", "Maintain weight"),
    )
    diet = st.segmented_control(
        "Diet",
        DIETS,
        default=saved.get("diet", "Vegetarian"),
    )
    allergies = st.pills(
        "Allergies",
        ALLERGY_OPTIONS,
        selection_mode="multi",
        default=saved.get("allergies") or [],
    )
    submitted = st.form_submit_button("Save profile", type="primary", width="stretch")

if submitted:
    if not goal or not diet:
        st.warning("Choose a health goal and a diet before saving.")
    else:
        try:
            st.session_state.profile = validate_profile(
                int(age),
                goal,
                diet,
                list(allergies or []),
            )
            st.session_state.meal_plan = None
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success("Profile saved for this session.", title="Profile saved")

profile = st.session_state.get("profile")
if profile:
    allergy_text = ", ".join(profile["allergies"]) if profile["allergies"] else "none reported"
    with st.container(border=True):
        st.markdown(
            f"**Age** {profile['age']}  \n"
            f"**Goal** {profile['goal']}  \n"
            f"**Diet** {profile['diet']}  \n"
            f"**Allergies** {allergy_text}"
        )
