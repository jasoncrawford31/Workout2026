# LTWD

Lift Til We Die

## Main App File

`streamlit_app.py`

## Local Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## CSV Storage

The app uses Google Sheets when Streamlit secrets are configured. If secrets are missing, it falls back to local CSV files in `data/`:

- `data/workouts.csv`
- `data/nutrition.csv`
- `data/progress.csv`

`workouts.csv` stores one row per exercise set. `nutrition.csv` stores one row per food entry with calculated calories and macros.

## Google Sheets Storage

Create one Google Sheet with these worksheet tabs:

- `workouts`
- `nutrition`
- `progress`

In Google Cloud, create a service account and JSON key. Share the Google Sheet with the service account `client_email` as an editor.

In Streamlit Cloud, open the app settings, go to **Secrets**, and paste values using `.streamlit/secrets.toml.example` as the template. Do not commit the real `secrets.toml` file to GitHub.
