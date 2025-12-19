import streamlit as st
import pandas as pd
import os
import sqlite3

# -------------------- APP CONFIG --------------------
st.set_page_config(page_title="Nova FitCoach AI", layout="wide")

# -------------------- PREMIUM UI (READABLE) --------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #203a43);
    color: white;
}

/* Card container */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    color: #222222;
}

/* Headings */
h1, h2, h3 {
    color: #1e3c72;
}

/* Paragraph text */
p, label, span, div {
    color: #222222;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

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

fitness_df = load_csv("fitness_plans_detailed_50_exercises.csv")
diet_df = load_csv("diet_plans_foods_50.csv")

# -------------------- SESSION STATE --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# -------------------- LOGIN --------------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:white;'>Nova FitCoach AI</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown("""
        <div class='card'>
            <h2>Welcome to Nova FitCoach AI 💪</h2>
            <p>Your AI-powered premium fitness, diet, and wellness assistant.</p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------- FITNESS --------------------
    elif st.session_state.page == "Fitness":
        st.markdown("<div class='card'><h2>🏋️ Fitness Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Goal", fitness_df["goal"].unique())
        level = st.selectbox("Fitness Level", fitness_df["level"].unique())
        duration = st.selectbox("Plan Duration", fitness_df["duration"].unique())

        if st.button("Generate Fitness Plan"):
            results = fitness_df[
                (fitness_df.goal == goal) &
                (fitness_df.level == level) &
                (fitness_df.duration == duration)
            ]

            for _, r in results.iterrows():
                st.markdown(f"""
                <div class='card'>
                    <h3>{r['exercise_name']}</h3>
                    <p>{r['exercise_explanation']}</p>
                    <p><b>Time:</b> {r['time_required']} &nbsp; | &nbsp; <b>Sets:</b> {r['sets']}</p>
                </div>
                """, unsafe_allow_html=True)

    # -------------------- DIET --------------------
    elif st.session_state.page == "Diet":
        st.markdown("<div class='card'><h2>🥗 Diet Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Goal", diet_df["goal"].unique())
        pref = st.selectbox("Diet Preference", diet_df["diet_preference"].unique())
        level = st.selectbox("Level", diet_df["level"].unique())

        if st.button("Generate Diet Plan"):
            r = diet_df[
                (diet_df.goal == goal) &
                (diet_df.diet_preference == pref) &
                (diet_df.level == level)
            ].iloc[0]

            st.markdown(f"""
            <div class='card'>
                <h3>🌅 Morning</h3>
                <p>{r['morning_meal']}</p>
                <h3>🍛 Afternoon</h3>
                <p>{r['afternoon_meal']}</p>
                <h3>🌙 Night</h3>
                <p>{r['night_meal']}</p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------- WELLNESS --------------------
    elif st.session_state.page == "Wellness":
        st.markdown("<div class='card'><h2>🧘 Mental Wellness</h2></div>", unsafe_allow_html=True)
        st.button("😊 Happy")
        st.button("🙂 Calm")
        st.button("😐 Neutral")
        st.button("😡 Stressed")
        st.text_area("Daily Journal")

    # -------------------- CALCULATOR --------------------
    elif st.session_state.page == "Calculator":
        st.markdown("<div class='card'><h2>📊 Health Calculator</h2></div>", unsafe_allow_html=True)

        weight = st.number_input("Weight (kg)", 1.0)
        height = st.number_input("Height (cm)", 1.0)
        age = st.number_input("Age", 1)

        if st.button("Calculate BMI"):
            bmi = weight / ((height / 100) ** 2)
            st.success(f"BMI: {bmi:.2f}")

    # -------------------- FEEDBACK --------------------
    elif st.session_state.page == "Feedback":
        st.markdown("<div class='card'><h2>💬 Feedback</h2></div>", unsafe_allow_html=True)

        category = st.selectbox("Category", ["General Comment", "Feature Request", "Bug Report", "Praise"])
        message = st.text_area("Message")

        if st.button("Send Feedback"):
            conn = sqlite3.connect("feedback.db")
            c = conn.cursor()
            c.execute("INSERT INTO feedback (category, message) VALUES (?, ?)", (category, message))
            conn.commit()
            conn.close()
            st.success("Feedback submitted successfully!")

    # -------------------- ABOUT --------------------
    elif st.session_state.page == "About Us":
        st.markdown("""
        <div class='card'>
            <h2>ℹ️ About Nova FitCoach AI</h2>
            <p>AI-powered fitness, diet, and mental wellness assistant.</p>
            <p><b>Creators:</b> Navketan Parab, Om Mohorkar, Vedant Malpure, Avishkar Manchare</p>
        </div>
        """, unsafe_allow_html=True)
