# NutriRAG

NutriRAG is a nutrition and wellness assistant for everyday eating. It saves a profile for the browser session, answers food questions from local guides, and builds a one-day meal plan from an Indian food table.

This is general nutrition education. It is not medical advice and does not replace a doctor or a dietitian.

## Run locally

Use Python 3.14.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Put your Groq key in `.env` as `GROQ_API_KEY`. That file is gitignored. Do not commit the key.

```powershell
py -3.14 -m streamlit run app.py
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

Pages:

- **Profile.** Age (16–80), health goal, diet, and allergies. Vegetarian includes dairy and excludes eggs, meat, and fish. Vegan excludes all animal foods. Eggetarian adds eggs.
- **Chat.** Ordinary food questions are answered from the PDFs in `documents/`, with the source file names shown. Diagnosis, medicine, dosage, and treatment questions are refused before any Groq call. The chat stays on screen until the browser session ends. Clear chat empties it.
- **Meal plan.** Breakfast, a morning snack, lunch, an evening snack, and dinner from `documents/indianfood.csv`. Foods are filtered by diet and allergies. Portions use per-100 g values from Indian Food Composition Tables 2017.

If the vector index is missing, rebuild it once:

```powershell
py -3.14 ingest.py
```

## Public link

A public URL with no login needs your own GitHub repository and a [Streamlit Community Cloud](https://share.streamlit.io) app.

1. Push this project to GitHub. Do not push `.env`.
2. In Streamlit Community Cloud, create an app from that repo. Set the main file to `app.py`.
3. In the app settings, add a secret:

```toml
GROQ_API_KEY = "your_groq_key_here"
```

The app reads that secret when the environment variable is empty. The free Cloud tier has a small memory limit. This app loads a sentence-transformer model for search, so the first Cloud deploy can run out of memory. If that happens, say so and the search step can be switched to a lighter index over the same PDFs. Local use does not depend on that change.

Screenshots for the exam are in `screenshots/`. The prompt log and test note are in `SUBMISSION.md`.
