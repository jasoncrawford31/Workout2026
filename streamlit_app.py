from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
WORKOUTS_CSV = DATA_DIR / "workouts.csv"
NUTRITION_CSV = DATA_DIR / "nutrition.csv"
PROGRESS_CSV = DATA_DIR / "progress.csv"

WORKOUT_COLUMNS = [
    "date",
    "workout_day",
    "workout_type",
    "exercise",
    "set_number",
    "reps",
    "weight_lbs",
    "notes",
    "duration_min",
    "effort",
]

NUTRITION_COLUMNS = [
    "date",
    "food",
    "quantity",
    "unit",
    "calories",
    "protein_g",
    "carbs_g",
    "fat_g",
    "fiber_g",
    "notes",
]

PROGRESS_COLUMNS = [
    "date",
    "body_weight_lbs",
    "waist_in",
    "body_fat_pct",
    "resting_hr",
    "sleep_hours",
    "energy",
    "notes",
]

TABLES = {
    "workouts": {"csv": WORKOUTS_CSV, "columns": WORKOUT_COLUMNS},
    "nutrition": {"csv": NUTRITION_CSV, "columns": NUTRITION_COLUMNS},
    "progress": {"csv": PROGRESS_CSV, "columns": PROGRESS_COLUMNS},
}

DEFAULT_SETTINGS = {
    "age": 61,
    "height_in": 70,
    "target_weight_lbs": 180,
    "target_waist_in": 36,
    "daily_calorie_target": 2100,
    "daily_protein_target_g": 160,
    "weekly_strength_sessions": 5,
    "weekly_cardio_sessions": 2,
}

WEEKLY_SPLIT = {
    "Monday": "Shoulders",
    "Tuesday": "Legs",
    "Wednesday": "Biceps & Triceps",
    "Thursday": "Back",
    "Friday": "Full Body",
}

PLANNED_EXERCISES = {
    "Monday": [
        "Seated dumbbell shoulder press",
        "Dumbbell lateral raise",
        "Rear delt fly",
        "Cable face pull",
        "Dumbbell shrug",
    ],
    "Tuesday": [
        "Leg press or squat",
        "Romanian deadlift",
        "Leg curl",
        "Standing calf raise",
    ],
    "Wednesday": [
        "Barbell or EZ-bar curl",
        "Incline dumbbell curl",
        "Cable rope pressdown",
        "Overhead triceps extension",
        "Close-grip push-up or bench press",
    ],
    "Thursday": [
        "Lat pulldown",
        "Seated cable row",
        "One-arm dumbbell row",
        "Straight-arm pulldown",
        "Back extension",
    ],
    "Friday": [
        "Goblet squat",
        "Dumbbell bench press",
        "Romanian deadlift",
        "Lat pulldown or row",
        "Farmer carry or plank",
    ],
}

WORKOUT_TYPES = [
    "Shoulders",
    "Legs",
    "Biceps & Triceps",
    "Back",
    "Full Body",
    "Cardio",
    "Mobility",
    "Recovery",
]

WORKOUT_DAYS = list(WEEKLY_SPLIT.keys())

FOOD_DATABASE = {
    "eggs": {"unit": "pieces", "base_qty": 1, "calories": 72, "protein_g": 6.3, "carbs_g": 0.4, "fat_g": 4.8, "fiber_g": 0},
    "cooked steel cut oats": {"unit": "cups", "base_qty": 1, "calories": 170, "protein_g": 6, "carbs_g": 29, "fat_g": 3, "fiber_g": 5},
    "ground flax": {"unit": "tbsp", "base_qty": 1, "calories": 37, "protein_g": 1.3, "carbs_g": 2, "fat_g": 3, "fiber_g": 1.9},
    "chia seeds": {"unit": "tbsp", "base_qty": 1, "calories": 58, "protein_g": 2, "carbs_g": 5, "fat_g": 3.7, "fiber_g": 4.1},
    "whole wheat bread": {"unit": "pieces", "base_qty": 1, "calories": 80, "protein_g": 4, "carbs_g": 14, "fat_g": 1.2, "fiber_g": 2},
    "raspberries": {"unit": "grams", "base_qty": 100, "calories": 52, "protein_g": 1.2, "carbs_g": 12, "fat_g": 0.7, "fiber_g": 6.5},
    "blueberries": {"unit": "grams", "base_qty": 100, "calories": 57, "protein_g": 0.7, "carbs_g": 14.5, "fat_g": 0.3, "fiber_g": 2.4},
    "chicken breast": {"unit": "grams", "base_qty": 100, "calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6, "fiber_g": 0},
    "lean sirloin": {"unit": "grams", "base_qty": 100, "calories": 210, "protein_g": 29, "carbs_g": 0, "fat_g": 10, "fiber_g": 0},
    "salmon": {"unit": "grams", "base_qty": 100, "calories": 208, "protein_g": 20, "carbs_g": 0, "fat_g": 13, "fiber_g": 0},
    "potatoes": {"unit": "grams", "base_qty": 100, "calories": 87, "protein_g": 1.9, "carbs_g": 20, "fat_g": 0.1, "fiber_g": 1.8},
    "cooked rice": {"unit": "cups", "base_qty": 1, "calories": 205, "protein_g": 4.3, "carbs_g": 45, "fat_g": 0.4, "fiber_g": 0.6},
    "dry pasta": {"unit": "grams", "base_qty": 100, "calories": 371, "protein_g": 13, "carbs_g": 75, "fat_g": 1.5, "fiber_g": 3.2},
    "peanut butter": {"unit": "tbsp", "base_qty": 1, "calories": 95, "protein_g": 3.5, "carbs_g": 3.5, "fat_g": 8, "fiber_g": 1},
    "Fairlife vanilla protein shake": {"unit": "serving", "base_qty": 1, "calories": 150, "protein_g": 30, "carbs_g": 4, "fat_g": 2.5, "fiber_g": 0},
    "spinach": {"unit": "cups", "base_qty": 1, "calories": 7, "protein_g": 0.9, "carbs_g": 1.1, "fat_g": 0.1, "fiber_g": 0.7},
    "broccoli": {"unit": "grams", "base_qty": 100, "calories": 35, "protein_g": 2.4, "carbs_g": 7.2, "fat_g": 0.4, "fiber_g": 3.3},
    "rice cakes": {"unit": "pieces", "base_qty": 1, "calories": 35, "protein_g": 0.7, "carbs_g": 7.3, "fat_g": 0.3, "fiber_g": 0.4},
    "almonds": {"unit": "grams", "base_qty": 28, "calories": 164, "protein_g": 6, "carbs_g": 6, "fat_g": 14, "fiber_g": 3.5},
    "pizza": {"unit": "pieces", "base_qty": 1, "calories": 285, "protein_g": 12, "carbs_g": 36, "fat_g": 10, "fiber_g": 2.5},
}


st.set_page_config(
    page_title="LTWD",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def ensure_csv(path: Path, columns: list[str], defaults: dict | None = None) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return

    if defaults:
        pd.DataFrame([defaults], columns=columns).to_csv(path, index=False)
    else:
        pd.DataFrame(columns=columns).to_csv(path, index=False)


def table_name_for_path(path: Path) -> str | None:
    for table_name, config in TABLES.items():
        if config["csv"] == path:
            return table_name
    return None


def google_sheets_enabled() -> bool:
    return (
        gspread is not None
        and Credentials is not None
        and "google_sheets" in st.secrets
        and "gcp_service_account" in st.secrets
        and bool(st.secrets["google_sheets"].get("spreadsheet_id"))
    )


def storage_status_label() -> str:
    if google_sheets_enabled():
        return "Storage: Google Sheets"
    return "Storage: local CSV fallback"


@st.cache_resource
def get_google_spreadsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=scopes,
    )
    client = gspread.authorize(credentials)
    return client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])


def get_google_worksheet(table_name: str, columns: list[str]):
    spreadsheet = get_google_spreadsheet()
    worksheets_by_title = {worksheet.title: worksheet for worksheet in spreadsheet.worksheets()}
    worksheet = worksheets_by_title.get(table_name)
    if worksheet is None:
        try:
            worksheet = spreadsheet.add_worksheet(title=table_name, rows=1000, cols=max(len(columns), 1))
        except gspread.exceptions.APIError as exc:
            if "already exists" not in str(exc):
                raise
            worksheet = spreadsheet.worksheet(table_name)

    values = worksheet.get_all_values()
    if not values:
        worksheet.update("A1", [columns])
    return worksheet


def load_google_sheet(table_name: str, columns: list[str]) -> pd.DataFrame:
    worksheet = get_google_worksheet(table_name, columns)
    values = worksheet.get_all_values()
    if not values:
        return pd.DataFrame(columns=columns)

    header = values[0]
    rows = values[1:]
    df = pd.DataFrame(rows, columns=header)
    for column in columns:
        if column not in df.columns:
            df[column] = None
    return df[columns]


def save_google_sheet(table_name: str, df: pd.DataFrame, columns: list[str]) -> None:
    worksheet = get_google_worksheet(table_name, columns)
    clean = df[columns].copy().fillna("")
    values = [columns] + clean.astype(str).values.tolist()
    worksheet.clear()
    worksheet.update("A1", values)


def load_csv(path: Path, columns: list[str], defaults: dict | None = None) -> pd.DataFrame:
    table_name = table_name_for_path(path)
    if table_name and google_sheets_enabled():
        try:
            return load_google_sheet(table_name, columns)
        except Exception as exc:
            st.warning(f"Google Sheets storage is not available right now, using local CSV instead. Details: {exc}")

    ensure_csv(path, columns, defaults)
    df = pd.read_csv(path)
    for column in columns:
        if column not in df.columns:
            df[column] = None
    return df[columns]


def save_csv(df: pd.DataFrame, path: Path, columns: list[str]) -> None:
    table_name = table_name_for_path(path)
    if table_name and google_sheets_enabled():
        try:
            save_google_sheet(table_name, df, columns)
            return
        except Exception as exc:
            st.warning(f"Could not save to Google Sheets, saving local CSV instead. Details: {exc}")

    df[columns].to_csv(path, index=False)


def append_rows(existing: pd.DataFrame, new_rows: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if new_rows.empty:
        return existing[columns]
    if existing.empty:
        return new_rows[columns].reset_index(drop=True)
    return pd.concat([existing[columns], new_rows[columns]], ignore_index=True)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    if not df.empty and "date" in df.columns:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def latest_value(df: pd.DataFrame, column: str):
    if df.empty or column not in df.columns:
        return None
    clean = parse_dates(df).dropna(subset=["date", column]).sort_values("date")
    if clean.empty:
        return None
    return clean.iloc[-1][column]


def delta_from_first(df: pd.DataFrame, column: str):
    clean = parse_dates(df).dropna(subset=["date", column]).sort_values("date")
    if len(clean) < 2:
        return None
    return clean.iloc[-1][column] - clean.iloc[0][column]


def week_filter(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    dated = parse_dates(df).dropna(subset=["date"])
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=6)
    return dated[dated["date"] >= start]


def format_delta(value, suffix=""):
    if value is None or pd.isna(value):
        return None
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}{suffix}"


def card_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.4rem; }
        div[data-testid="stMetric"] {
            background: #f7f8fa;
            border: 1px solid #e4e7ec;
            border-radius: 8px;
            padding: 14px 16px;
        }
        .focus-note {
            border-left: 4px solid #1f7a5f;
            background: #f3faf7;
            padding: 12px 14px;
            border-radius: 6px;
            margin: 4px 0 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def planned_workout_for_day(day: str) -> str:
    return WEEKLY_SPLIT.get(day, "Recovery / optional easy cardio")


def planned_exercises_for_day(day: str) -> list[str]:
    return PLANNED_EXERCISES.get(day, [])


def calculate_food_macros(food: str, quantity: float) -> dict[str, float]:
    item = FOOD_DATABASE[food]
    factor = quantity / item["base_qty"]
    return {
        "calories": item["calories"] * factor,
        "protein_g": item["protein_g"] * factor,
        "carbs_g": item["carbs_g"] * factor,
        "fat_g": item["fat_g"] * factor,
        "fiber_g": item["fiber_g"] * factor,
    }


def nutrition_totals_for_date(nutrition: pd.DataFrame, target_date: date) -> dict[str, float]:
    if nutrition.empty:
        return {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0, "fiber_g": 0}
    dated = parse_dates(nutrition).dropna(subset=["date"])
    day_rows = dated[dated["date"].dt.date == target_date]
    return {
        key: float(pd.to_numeric(day_rows[key], errors="coerce").fillna(0).sum())
        for key in ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g"]
    }


def seven_day_daily_average(nutrition: pd.DataFrame, column: str) -> float:
    if nutrition.empty:
        return 0.0
    dated = week_filter(nutrition)
    if dated.empty:
        return 0.0
    dated = dated.copy()
    dated[column] = pd.to_numeric(dated[column], errors="coerce").fillna(0)
    daily = dated.groupby(dated["date"].dt.date)[column].sum()
    return float(daily.sum() / 7)


def render_weekly_split() -> None:
    split_rows = pd.DataFrame(
        [{"Day": day, "Workout": workout} for day, workout in WEEKLY_SPLIT.items()]
    )
    st.table(split_rows)


def render_dashboard(
    workouts: pd.DataFrame,
    nutrition: pd.DataFrame,
    progress: pd.DataFrame,
    settings: dict,
) -> None:
    st.subheader("Current Status")
    st.markdown(
        '<div class="focus-note">Goal focus: reduce waist size while preserving and building lean muscle through steady protein intake, progressive strength work, sleep, and moderate cardio.</div>',
        unsafe_allow_html=True,
    )

    latest_weight = latest_value(progress, "body_weight_lbs")
    latest_waist = latest_value(progress, "waist_in")
    weight_delta = delta_from_first(progress, "body_weight_lbs")
    waist_delta = delta_from_first(progress, "waist_in")
    week_workouts = week_filter(workouts)
    today_totals = nutrition_totals_for_date(nutrition, date.today())
    avg_calories = seven_day_daily_average(nutrition, "calories")
    avg_protein = seven_day_daily_average(nutrition, "protein_g")

    strength_count = 0
    cardio_count = 0
    if not week_workouts.empty:
        types = week_workouts["workout_type"].fillna("").str.lower()
        strength_count = int(types.str.contains("shoulders|legs|biceps|triceps|back|full body|strength|weights|resistance").sum())
        cardio_count = int(types.str.contains("cardio|walk|bike|run|swim|zone").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Weight", f"{latest_weight:.1f} lb" if latest_weight else "No data", format_delta(weight_delta, " lb"))
    c2.metric("Current Waist", f"{latest_waist:.1f} in" if latest_waist else "No data", format_delta(waist_delta, " in"))
    c3.metric("Calories Today", f"{today_totals['calories']:.0f}")
    c4.metric("Protein Today", f"{today_totals['protein_g']:.0f} g", f"target {int(settings['daily_protein_target_g'])} g")

    c5, c6, c7 = st.columns(3)
    c5.metric("Fiber Today", f"{today_totals['fiber_g']:.1f} g")
    c6.metric("7-Day Avg Calories", f"{avg_calories:.0f}", f"target {int(settings['daily_calorie_target'])}")
    c7.metric("7-Day Avg Protein", f"{avg_protein:.0f} g")

    c8, c9, c10 = st.columns(3)
    c8.metric("Strength Sessions", f"{strength_count}/{int(settings['weekly_strength_sessions'])}", "last 7 days")
    c9.metric("Cardio Sessions", f"{cardio_count}/{int(settings['weekly_cardio_sessions'])}", "last 7 days")
    c10.metric("Logged Sets", f"{len(week_workouts)}", "last 7 days")

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Body Trend")
        trend = parse_dates(progress).dropna(subset=["date"])
        if trend.empty:
            st.info("Add progress entries to see weight and waist trends.")
        else:
            chart_cols = [col for col in ["body_weight_lbs", "waist_in", "body_fat_pct"] if trend[col].notna().any()]
            st.line_chart(trend.set_index("date")[chart_cols])

    with right:
        st.subheader("Weekly Split")
        render_weekly_split()
        today_name = date.today().strftime("%A")
        st.info(f"Today's plan: {planned_workout_for_day(today_name)}")

        st.subheader("This Week's Priorities")
        st.write("1. Hit protein target on most days.")
        st.write("2. Complete the Monday-Friday lifting split with controlled effort.")
        st.write("3. Keep waist trend moving down, even if weight moves slowly.")
        st.write("4. Add easy cardio or brisk walking around the lifting schedule.")
        st.caption("For a 61-year-old lifter, consistency and recovery beat extreme cuts.")


def render_workout_log(workouts: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Workout Log")
    st.caption("Choose the workout day, then log reps and weight inside each exercise section.")

    selected_day = st.selectbox("Workout day", WORKOUT_DAYS, index=0)
    workout_type = planned_workout_for_day(selected_day)
    planned_exercises = planned_exercises_for_day(selected_day)

    left, right = st.columns([1, 1])
    with left:
        st.markdown(f"**Planned workout:** {workout_type}")
        st.table(pd.DataFrame({"Exercise": planned_exercises}))
    with right:
        st.markdown("**Weekly split**")
        render_weekly_split()

    with st.form("workout_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        workout_date = c1.date_input("Date", value=date.today())
        duration = c2.number_input("Duration minutes", min_value=0, max_value=300, value=45, step=5)
        effort = c3.slider("Overall effort", 1, 10, 7, help="Aim for challenging but controlled work most days.")

        st.markdown("**Exercise sets**")
        logged_rows = []
        for exercise_index, exercise in enumerate(planned_exercises):
            with st.expander(exercise, expanded=exercise_index == 0):
                set_count = st.number_input(
                    "Number of sets",
                    min_value=1,
                    max_value=8,
                    value=3,
                    step=1,
                    key=f"{selected_day}_{exercise_index}_set_count",
                )
                for set_number in range(1, int(set_count) + 1):
                    c_reps, c_weight, c_notes = st.columns([1, 1, 2])
                    reps = c_reps.number_input(
                        f"Set {set_number} reps",
                        min_value=0,
                        max_value=100,
                        value=0,
                        step=1,
                        key=f"{selected_day}_{exercise_index}_{set_number}_reps",
                    )
                    weight = c_weight.number_input(
                        f"Set {set_number} weight",
                        min_value=0.0,
                        max_value=1000.0,
                        value=0.0,
                        step=2.5,
                        key=f"{selected_day}_{exercise_index}_{set_number}_weight",
                    )
                    set_notes = c_notes.text_input(
                        f"Set {set_number} notes",
                        key=f"{selected_day}_{exercise_index}_{set_number}_notes",
                        placeholder="optional",
                    )
                    if reps > 0 or weight > 0 or set_notes.strip():
                        logged_rows.append(
                            {
                                "date": workout_date.isoformat(),
                                "workout_day": selected_day,
                                "workout_type": workout_type,
                                "exercise": exercise,
                                "set_number": set_number,
                                "reps": reps,
                                "weight_lbs": weight,
                                "notes": set_notes,
                                "duration_min": duration,
                                "effort": effort,
                            }
                        )

        workout_notes = st.text_area("Workout notes", placeholder="Overall energy, soreness, technique, progression...")
        submitted = st.form_submit_button("Save Workout")

    if submitted:
        new_rows = pd.DataFrame(logged_rows, columns=WORKOUT_COLUMNS)
        if not new_rows.empty and workout_notes.strip():
            first_index = new_rows.index[0]
            first_note = new_rows.loc[first_index, "notes"]
            new_rows.loc[first_index, "notes"] = f"{first_note} | {workout_notes}".strip(" |")
        workouts = append_rows(workouts, new_rows, WORKOUT_COLUMNS)
        save_csv(workouts, WORKOUTS_CSV, WORKOUT_COLUMNS)
        st.success(f"Saved {len(new_rows)} sets for {workout_type}.")

    st.subheader("Recent Workout Sets")
    if workouts.empty:
        st.info("No workout sets logged yet.")
    else:
        recent_cols = ["date", "workout_day", "workout_type", "exercise", "set_number", "reps", "weight_lbs", "notes"]
        st.dataframe(workouts[recent_cols].tail(25), hide_index=True, use_container_width=True)
    return load_csv(WORKOUTS_CSV, WORKOUT_COLUMNS)


def render_nutrition_log(nutrition: pd.DataFrame, settings: dict) -> pd.DataFrame:
    st.subheader("Nutrition Log")
    st.caption("Select a food, enter the quantity, and the app calculates calories and macros.")

    with st.form("nutrition_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 1.4, 1])
        entry_date = c1.date_input("Date", value=date.today(), key="nutrition_date")
        food = c2.selectbox("Food", list(FOOD_DATABASE.keys()))
        unit = FOOD_DATABASE[food]["unit"]
        quantity = c3.number_input(f"Quantity ({unit})", min_value=0.0, max_value=5000.0, value=1.0, step=0.25)

        macros = calculate_food_macros(food, quantity)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Calories", f"{macros['calories']:.0f}")
        m2.metric("Protein", f"{macros['protein_g']:.1f} g")
        m3.metric("Carbs", f"{macros['carbs_g']:.1f} g")
        m4.metric("Fat", f"{macros['fat_g']:.1f} g")
        m5.metric("Fiber", f"{macros['fiber_g']:.1f} g")

        notes = st.text_input("Notes", placeholder="optional")
        submitted = st.form_submit_button("Add Food")

    if submitted:
        new_row = pd.DataFrame(
            [{
                "date": entry_date.isoformat(),
                "food": food,
                "quantity": quantity,
                "unit": unit,
                "calories": round(macros["calories"], 1),
                "protein_g": round(macros["protein_g"], 1),
                "carbs_g": round(macros["carbs_g"], 1),
                "fat_g": round(macros["fat_g"], 1),
                "fiber_g": round(macros["fiber_g"], 1),
                "notes": notes,
            }]
        )
        nutrition = append_rows(nutrition, new_row, NUTRITION_COLUMNS)
        save_csv(nutrition, NUTRITION_CSV, NUTRITION_COLUMNS)
        st.success(f"Added {quantity:g} {unit} of {food}.")

    today_totals = nutrition_totals_for_date(nutrition, date.today())
    st.subheader("Daily Totals")
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Calories Today", f"{today_totals['calories']:.0f}")
    d2.metric("Protein Today", f"{today_totals['protein_g']:.1f} g")
    d3.metric("Carbs Today", f"{today_totals['carbs_g']:.1f} g")
    d4.metric("Fat Today", f"{today_totals['fat_g']:.1f} g")
    d5.metric("Fiber Today", f"{today_totals['fiber_g']:.1f} g")

    if not nutrition.empty:
        chart = parse_dates(nutrition).dropna(subset=["date"]).set_index("date")
        daily_chart = chart.groupby(chart.index.date)[["calories", "protein_g", "fiber_g"]].sum()
        st.line_chart(daily_chart)

    st.subheader("Food Entries")
    edited_nutrition = st.data_editor(nutrition, num_rows="dynamic", use_container_width=True, key="nutrition_editor")
    if st.button("Save Nutrition Table"):
        save_csv(edited_nutrition, NUTRITION_CSV, NUTRITION_COLUMNS)
        st.success("Nutrition table saved.")
    return load_csv(NUTRITION_CSV, NUTRITION_COLUMNS)


def render_progress_tracking(progress: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Progress Tracking")
    with st.form("progress_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        entry_date = c1.date_input("Date", value=date.today(), key="progress_date")
        body_weight = c2.number_input("Body weight, lb", min_value=0.0, max_value=500.0, value=190.0, step=0.5)
        waist = c3.number_input("Waist, inches", min_value=0.0, max_value=80.0, value=40.0, step=0.25)
        c4, c5, c6 = st.columns(3)
        body_fat = c4.number_input("Body fat %", min_value=0.0, max_value=60.0, value=0.0, step=0.5)
        resting_hr = c5.number_input("Resting heart rate", min_value=0, max_value=180, value=65)
        sleep = c6.number_input("Sleep hours", min_value=0.0, max_value=14.0, value=7.0, step=0.25)
        energy = st.slider("Energy", 1, 10, 7)
        notes = st.text_area("Notes", placeholder="Photos, belt notch, soreness, mood...")
        submitted = st.form_submit_button("Add Progress Entry")

    if submitted:
        new_row = pd.DataFrame(
            [{
                "date": entry_date.isoformat(),
                "body_weight_lbs": body_weight,
                "waist_in": waist,
                "body_fat_pct": body_fat if body_fat else None,
                "resting_hr": resting_hr,
                "sleep_hours": sleep,
                "energy": energy,
                "notes": notes,
            }]
        )
        progress = append_rows(progress, new_row, PROGRESS_COLUMNS)
        save_csv(progress, PROGRESS_CSV, PROGRESS_COLUMNS)
        st.success("Progress entry added.")

    dated = parse_dates(progress).dropna(subset=["date"])
    if not dated.empty:
        st.line_chart(dated.set_index("date")[[col for col in ["body_weight_lbs", "waist_in", "sleep_hours"] if col in dated.columns]])

    st.data_editor(progress, num_rows="dynamic", use_container_width=True, key="progress_editor")
    if st.button("Save Progress Table"):
        save_csv(st.session_state.progress_editor, PROGRESS_CSV, PROGRESS_COLUMNS)
        st.success("Progress table saved.")
    return load_csv(PROGRESS_CSV, PROGRESS_COLUMNS)


def main() -> None:
    card_css()
    workouts = load_csv(WORKOUTS_CSV, WORKOUT_COLUMNS)
    nutrition = load_csv(NUTRITION_CSV, NUTRITION_COLUMNS)
    progress = load_csv(PROGRESS_CSV, PROGRESS_COLUMNS)
    settings = DEFAULT_SETTINGS.copy()

    st.title("LTWD")
    st.caption("Lift Til We Die")
    st.caption(storage_status_label())

    tabs = st.tabs(["Dashboard", "Workout Log", "Nutrition Log", "Progress Tracking"])
    with tabs[0]:
        render_dashboard(workouts, nutrition, progress, settings)
    with tabs[1]:
        workouts = render_workout_log(workouts)
    with tabs[2]:
        nutrition = render_nutrition_log(nutrition, settings)
    with tabs[3]:
        progress = render_progress_tracking(progress)


if __name__ == "__main__":
    main()
