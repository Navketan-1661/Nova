import streamlit as st
import pandas as pd
import os
import sqlite3

# -------------------- APP CONFIG --------------------
st.set_page_config(page_title="Nova FitCoach AI", layout="wide")

# -------------------- DATABASE SETUP --------------------
def init_db():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------- SAFE CSV LOADING --------------------
@st.cache_data
def load_csv(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    return None

# 🔁 RENAMED FILES
fitness_df = load_csv("fitness_plans_detailed_50_exercises.csv")
diet_df = load_csv("diet_plans_foods_50.csv")

# -------------------- SESSION STATE --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# -------------------- LOGIN --------------------
if not st.session_state.logged_in:
    st.title("Nova FitCoach AI – Login")
    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

# ==================== MAIN APP ====================
else:
    # -------------------- SIDEBAR --------------------
    with st.sidebar:
        st.title("☰ Menu")
        st.session_state.page = st.radio(
            "Navigate",
            ["Dashboard", "Fitness", "Diet", "Wellness", "Calculator", "Feedback", "About Us"]
        )

    # -------------------- DASHBOARD --------------------
    if st.session_state.page == "Dashboard":
        st.header("📌 Dashboard")
        st.success("Welcome to Nova FitCoach AI 💪")

    # -------------------- FITNESS --------------------
    elif st.session_state.page == "Fitness":
        st.header("🏋️ Fitness Planner")

        if fitness_df is None:
            st.error("Fitness data file not found.")
        else:
            goal = st.selectbox("Goal", fitness_df["goal"].unique())
            level = st.selectbox("Fitness Level", fitness_df["level"].unique())
            duration = st.selectbox("Plan Duration", fitness_df["duration"].unique())

            if st.button("Generate Fitness Plan"):
                results = fitness_df[
                    (fitness_df.goal == goal) &
                    (fitness_df.level == level) &
                    (fitness_df.duration == duration)
                ]

                if not results.empty:
                    for _, r in results.iterrows():
                        st.subheader(r["exercise_name"])
                        st.write(r["exercise_explanation"])
                        st.write(f"⏱ **Time:** {r['time_required']}")
                        st.write(f"🔁 **Sets:** {r['sets']}")
                        st.divider()
                else:
                    st.warning("No fitness plan found.")

    # -------------------- DIET --------------------
    elif st.session_state.page == "Diet":
        st.header("🥗 Diet Planner")

        if diet_df is None:
            st.error("Diet data file not found.")
        else:
            goal = st.selectbox("Goal", diet_df["goal"].unique())
            preference = st.selectbox("Diet Preference", diet_df["diet_preference"].unique())
            level = st.selectbox("Level", diet_df["level"].unique())

            if st.button("Generate Diet Plan"):
                results = diet_df[
                    (diet_df.goal == goal) &
                    (diet_df.diet_preference == preference) &
                    (diet_df.level == level)
                ]

                if not results.empty:
                    r = results.iloc[0]
                    st.write(f"🌅 **Morning:** {r['morning_meal']}")
                    st.write(f"🍛 **Afternoon:** {r['afternoon_meal']}")
                    st.write(f"🌙 **Night:** {r['night_meal']}")
                else:
                    st.warning("No diet plan found.")

    # -------------------- WELLNESS --------------------
    elif st.session_state.page == "Wellness":
        st.header("🧘 Mental Wellness")
        st.write("How are you feeling today?")
        st.button("😊 Happy")
        st.button("🙂 Calm")
        st.button("😐 Neutral")
        st.button("😡 Stressed")

        journal = st.text_area("Daily Journal")
        if st.button("Log Entry"):
            st.success("Wellness entry saved.")

    # -------------------- CALCULATOR --------------------
    elif st.session_state.page == "Calculator":
        st.header("📊 Health Calculator")

        weight = st.number_input("Weight (kg)", min_value=1.0)
        height = st.number_input("Height (cm)", min_value=1.0)
        age = st.number_input("Age", min_value=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
        )

        if st.button("Calculate"):
            bmi = weight / ((height / 100) ** 2)
            st.success(f"📏 BMI: {bmi:.2f}")

            bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
            factors = {
                "Sedentary": 1.2,
                "Lightly Active": 1.375,
                "Moderately Active": 1.55,
                "Very Active": 1.725,
                "Extra Active": 1.9,
            }
            calories = bmr * factors[activity]
            st.success(f"🔥 Daily Calories: {int(calories)} kcal")

    # -------------------- FEEDBACK --------------------
    elif st.session_state.page == "Feedback":
        st.header("💬 Feedback")

        category = st.selectbox(
            "Category",
            ["General Comment", "Feature Request", "Bug Report", "Praise"]
        )
        message = st.text_area("Message")

        if st.button("Send Feedback"):
            conn = sqlite3.connect("feedback.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO feedback (category, message) VALUES (?, ?)",
                (category, message)
            )
            conn.commit()
            conn.close()
            st.success("Feedback submitted successfully!")

    # -------------------- ABOUT --------------------
    elif st.session_state.page == "About Us":
        st.header("ℹ️ About Nova FitCoach AI")
        st.write("AI-powered fitness, diet, and mental wellness assistant.")
        st.write("Creators:")
        st.write("- Navketan Parab")
        st.write("- Om Mohorkar")
        st.write("- Vedant Malpure")
        st.write("- Avishkar Manchare")
