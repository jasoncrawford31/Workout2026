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

The app stores local CSV data in `data/`:

- `data/workouts.csv`
- `data/nutrition.csv`
- `data/progress.csv`

`workouts.csv` stores one row per exercise set. `nutrition.csv` stores one row per food entry with calculated calories and macros.
