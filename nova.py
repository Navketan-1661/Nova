import streamlit as st
import pandas as pd
import os
import sqlite3

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Nova FitCoach AI",
    layout="wide",
    page_icon="💪"
)

# ==================== GLOBAL STYLES ====================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #203a43);
    padding: 20px;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 26px;
    margin-bottom: 24px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.2);
}

h1, h2, h3 {
    color: #1e3c72;
}

label, p {
    color: #111827 !important;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e3a8a);
}

div[data-testid="stSuccess"] {
    background-color: #dcfce7;
    color: #065f46;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
def init_db():
    conn = sqlite3.connect("feedback.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==================== LOAD CSV ====================
@st.cache_data
def load_csv(file):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()

fitness_df = load_csv("fitness_plans_detailed_50_exercises.csv")
diet_df = load_csv("diet_plans_foods_50.csv")

# ==================== SESSION ====================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("page", "Dashboard")

# ==================== LOGIN ====================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;color:white;'>Nova FitCoach AI</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.text_input("Username")
    st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== MAIN APP ====================
else:
    # ---------- SIDEBAR ----------
    with st.sidebar:
        st.markdown("## ☰ Navigation")
        st.session_state.page = st.radio(
            "",
            ["Dashboard", "Fitness", "Diet", "Wellness", "Calculator", "Feedback", "About Us"]
        )

    # ---------- DASHBOARD ----------
    if st.session_state.page == "Dashboard":
        st.markdown("""
        <div class="card">
            <h2>Welcome 👋</h2>
            <p>Your AI-powered assistant for Fitness, Diet & Mental Wellness.</p>
            <p>Use the menu to explore personalized plans.</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- FITNESS ----------
    elif st.session_state.page == "Fitness":
        st.markdown("<div class='card'><h2>🏋️ Fitness Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Fitness Goal", fitness_df["goal"].unique())
        level = st.selectbox("Difficulty Level", fitness_df["level"].unique())
        duration = st.selectbox("Workout Duration", fitness_df["duration"].unique())

        if st.button("Generate Fitness Plan"):
            plans = fitness_df[
                (fitness_df.goal == goal) &
                (fitness_df.level == level) &
                (fitness_df.duration == duration)
            ]

            if plans.empty:
                st.warning("No plan found for selected options.")
            else:
                for _, r in plans.iterrows():
                    st.markdown(f"""
                    <div class="card">
                        <h3>{r['exercise_name']}</h3>
                        <p>{r['exercise_explanation']}</p>
                        <p><b>⏱ Time:</b> {r['time_required']} |
                           <b>🔁 Sets:</b> {r['sets']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # ---------- DIET ----------
    elif st.session_state.page == "Diet":
        st.markdown("<div class='card'><h2>🥗 Diet Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Diet Goal", diet_df["goal"].unique())
        pref = st.selectbox("Diet Preference", diet_df["diet_preference"].unique())
        level = st.selectbox("Activity Level", diet_df["level"].unique())

        if st.button("Generate Diet Plan"):
            plans = diet_df[
                (diet_df.goal == goal) &
                (diet_df.diet_preference == pref) &
                (diet_df.level == level)
            ]

            if plans.empty:
                st.warning("No diet plan available.")
            else:
                r = plans.iloc[0]
                st.markdown(f"""
                <div class="card">
                    <h3>🌅 Morning Meal</h3>
                    <p>{r['morning_meal']}</p>
                    <h3>🍛 Afternoon Meal</h3>
                    <p>{r['afternoon_meal']}</p>
                    <h3>🌙 Night Meal</h3>
                    <p>{r['night_meal']}</p>
                </div>
                """, unsafe_allow_html=True)

    # ---------- WELLNESS ----------
    elif st.session_state.page == "Wellness":
        st.markdown("<div class='card'><h2>🧘 Mental Wellness</h2></div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.button("😊 Happy")
        col2.button("🙂 Calm")
        col3.button("😐 Neutral")
        col4.button("😡 Stressed")

        st.text_area("📝 Daily Journal", height=120)

    # ---------- CALCULATOR ----------
    elif st.session_state.page == "Calculator":
        st.markdown("<div class='card'><h2>📊 BMI Calculator</h2></div>", unsafe_allow_html=True)

        weight = st.number_input("Weight (kg)", min_value=1.0)
        height = st.number_input("Height (cm)", min_value=1.0)

        if st.button("Calculate BMI"):
            bmi = weight / ((height / 100) ** 2)
            st.success(f"Your BMI is **{bmi:.2f}**")

    # ---------- FEEDBACK ----------
    elif st.session_state.page == "Feedback":
        st.markdown("<div class='card'><h2>💬 Feedback</h2></div>", unsafe_allow_html=True)

        category = st.selectbox("Feedback Type", ["General", "Feature", "Bug", "Praise"])
        message = st.text_area("Your Message")

        if st.button("Submit Feedback"):
            conn = sqlite3.connect("feedback.db")
            conn.execute(
                "INSERT INTO feedback (category, message) VALUES (?, ?)",
                (category, message)
            )
            conn.commit()
            conn.close()
            st.success("Thank you for your feedback!")

    # ---------- ABOUT ----------
    elif st.session_state.page == "About Us":
        st.markdown("""
        <div class="card">
            <h2>About Nova FitCoach AI</h2>
            <p>An AI-powered platform for fitness, nutrition, and mental wellness.</p>
            <p><b>Team:</b> Navketan • Om • Vedant • Avishkar</p>
        </div>
        """, unsafe_allow_html=True)
