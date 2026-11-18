import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planner import PlannerError, build_meal_plan

st.caption(
    "One day of meals from the Indian food table, filtered by the diet and allergies in your profile."
)

profile = st.session_state.get("profile")
if profile:
    allergy_text = ", ".join(profile["allergies"]) if profile["allergies"] else "none reported"
    st.caption(
        f"Profile: age {profile['age']}, {profile['goal'].lower()}, "
        f"{profile['diet'].lower()}, allergies {allergy_text}."
    )
else:
    st.info(
        "Save a profile on the Profile page. The meal plan uses that diet and those allergies.",
        title="Profile not saved",
    )

if st.button("Build meal plan", type="primary", width="stretch"):
    if not profile:
        st.warning("Save a profile before building a meal plan.")
    else:
        try:
            st.session_state.meal_plan = build_meal_plan(profile)
        except PlannerError as exc:
            st.session_state.meal_plan = None
            st.error(str(exc))

plan = st.session_state.get("meal_plan")
if plan and profile:
    with st.container(horizontal=True):
        st.metric("Calories", f"{plan.total_calories:.0f} kcal")
        st.metric("Protein", f"{plan.total_protein:.0f} g")
        st.metric("Target", f"{plan.calorie_target} kcal")

    current_meal = None
    for item in plan.items:
        if item.meal != current_meal:
            st.subheader(item.meal)
            current_meal = item.meal
        st.markdown(
            f"**{item.food_name}**  \n"
            f"{item.grams} g · {round(item.calories)} kcal · "
            f"{item.protein_g:.1f} g protein · {item.source}"
        )
    st.caption(plan.note)
