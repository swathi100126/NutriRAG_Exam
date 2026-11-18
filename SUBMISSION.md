# NutriRAG submission notes

## Prompt log

Prompts that built the first Chroma search app are not in this chat. Add those earlier prompts above this list if the examiner wants the full history. The prompts below are the ones in this session, in order.

1. Safety and usability criteria, plus the submission list (live link, five screenshots, prompt log, and a 150–200 word test note). A plan was written for a visible disclaimer, a refusal before any model call, session chat with source file names, a profile form, and a one-day meal plan. The app code was not changed in that step.
2. Implement that plan. The app now shows the disclaimer on every page, refuses diagnosis and medicine questions, keeps the chat for the browser session, saves a profile, builds a meal plan from the Indian food table, and includes the screenshots and this note.

## Screenshots

- `screenshots/01_profile_form.png` — profile form, saved for the session
- `screenshots/02_grounded_answer.png` — protein answer with the source file
- `screenshots/03_meal_plan.png` — one-day meal plan
- `screenshots/04_refused_question.png` — metformin question refused, with the earlier answer still on screen
- `screenshots/05_mobile_view.png` — the same profile form at phone width

## Test note

NutriRAG was tested in the browser with a saved profile: age 28, lose weight, vegetarian, and a peanut allergy.

For "What are good vegetarian protein sources?" the expected result was a guide-based answer that named its source and respected the peanut allergy. The app listed lentils, chickpeas, dairy foods, and almonds, said to avoid peanuts, and cited Vegetarian Protein Sources.pdf.

For the meal plan, the expected result was one day with grams, calories, protein, and IFCT 2017, and no peanuts, eggs, meat, or fish. The plan used rice, milk, paneer, vegetables, almond, wheat flour, and green gram, about 1684 kcal against a 1600 kcal target.

For "What dose of metformin should I take?" the expected result was a refusal with no dose, and the earlier answer still on screen. The app said it cannot help with diagnosis, medicines, dosages, or treatment, and to consult a doctor or a registered dietitian. The protein answer stayed above that reply.

One limitation: portions come from per-100 g IFCT values, so the 40 g almond snack is 244 kcal and can exceed its share of the calorie target. This is a general eating pattern, not a clinical diet.

## Live link

A public URL that opens without login still needs your GitHub repository and a Streamlit Community Cloud app, with `GROQ_API_KEY` stored only in the Cloud secrets. The steps are in `README.md`. This session cannot create that URL without those accounts.
