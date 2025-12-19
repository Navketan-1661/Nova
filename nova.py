import streamlit as st
import pandas as pd
import os
import sqlite3

# -------------------- APP CONFIG --------------------
st.set_page_config(page_title="Nova FitCoach AI", layout="wide")

# -------------------- SAFE + READABLE UI --------------------
st.markdown("""
<style>

/* ===== APP BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #203a43);
    padding: 20px;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: white !important;
}

/* ===== MAIN CONTENT TEXT ===== */
label, span, p {
    color: #1f2937 !important;
    font-weight: 500;
}

/* ===== INPUTS ===== */
input, textarea, select {
    color: #111827 !important;
    background-color: #f9fafb !important;
}

/* ===== CARDS ===== */
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

/* ===== HEADERS ===== */
h1, h2, h3 {
    color: #1e3c72 !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white !important;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e3a8a);
}

/* ===== SUCCESS MESSAGE ===== */
div[data-testid="stSuccess"] {
    background-color: #dcfce7;
    color: #065f46 !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATABASE --------------------
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

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_csv(file):
    return pd.read_csv(file) if os.path.exists(file) else None

fitness_df = load_csv("fitness_plans_detailed_50_exercises.csv")
diet_df = load_csv("diet_plans_foods_50.csv")

# -------------------- SESSION STATE --------------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("page", "Dashboard")

# -------------------- LOGIN --------------------
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
        st.markdown("## ☰ Menu")
        st.session_state.page = st.radio(
            "Navigation",
            ["Dashboard", "Fitness", "Diet", "Wellness", "Calculator", "Feedback", "About Us"],
            label_visibility="collapsed"
        )

    # ---------- DASHBOARD ----------
    if st.session_state.page == "Dashboard":
        st.markdown("""
        <div class='card'>
            <h2>Welcome 👋</h2>
            <p>Your AI-powered fitness, diet, and wellness assistant.</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- FITNESS ----------
    elif st.session_state.page == "Fitness":
        st.markdown("<div class='card'><h2>🏋️ Fitness Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Goal", fitness_df["goal"].unique())
        level = st.selectbox("Level", fitness_df["level"].unique())
        duration = st.selectbox("Duration", fitness_df["duration"].unique())

        if st.button("Generate Plan"):
            rows = fitness_df[(fitness_df.goal == goal) &
                              (fitness_df.level == level) &
                              (fitness_df.duration == duration)]
            for _, r in rows.iterrows():
                st.markdown(f"""
                <div class='card'>
                    <h3>{r['exercise_name']}</h3>
                    <p>{r['exercise_explanation']}</p>
                    <p><b>Time:</b> {r['time_required']} | <b>Sets:</b> {r['sets']}</p>
                </div>
                """, unsafe_allow_html=True)

    # ---------- DIET ----------
    elif st.session_state.page == "Diet":
        st.markdown("<div class='card'><h2>🥗 Diet Planner</h2></div>", unsafe_allow_html=True)

        goal = st.selectbox("Goal", diet_df["goal"].unique())
        pref = st.selectbox("Diet Preference", diet_df["diet_preference"].unique())
        level = st.selectbox("Level", diet_df["level"].unique())

        if st.button("Generate Diet"):
            r = diet_df[(diet_df.goal == goal) &
                        (diet_df.diet_preference == pref) &
                        (diet_df.level == level)].iloc[0]

            st.markdown(f"""
            <div class='card'>
                <h3>🌅 Morning</h3><p>{r['morning_meal']}</p>
                <h3>🍛 Afternoon</h3><p>{r['afternoon_meal']}</p>
                <h3>🌙 Night</h3><p>{r['night_meal']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------- WELLNESS ----------
    elif st.session_state.page == "Wellness":
        st.markdown("<div class='card'><h2>🧘 Wellness</h2></div>", unsafe_allow_html=True)
        st.button("😊 Happy")
        st.button("🙂 Calm")
        st.button("😐 Neutral")
        st.button("😡 Stressed")
        st.text_area("Journal")

    # ---------- CALCULATOR ----------
    elif st.session_state.page == "Calculator":
        st.markdown("<div class='card'><h2>📊 Calculator</h2></div>", unsafe_allow_html=True)
        w = st.number_input("Weight (kg)", min_value=1.0)
        h = st.number_input("Height (cm)", min_value=1.0)
        if st.button("Calculate BMI"):
            bmi = w / ((h / 100) ** 2)
            st.success(f"BMI: {bmi:.2f}")

    # ---------- FEEDBACK ----------
    elif st.session_state.page == "Feedback":
        st.markdown("<div class='card'><h2>💬 Feedback</h2></div>", unsafe_allow_html=True)
        cat = st.selectbox("Category", ["General", "Feature", "Bug", "Praise"])
        msg = st.text_area("Message")
        if st.button("Send"):
            conn = sqlite3.connect("feedback.db")
            conn.execute("INSERT INTO feedback (category, message) VALUES (?,?)", (cat, msg))
            conn.commit()
            conn.close()
            st.success("Feedback sent successfully!")

    # ---------- ABOUT ----------
    elif st.session_state.page == "About Us":
        st.markdown("""
        <div class='card'>
            <h2>About Nova FitCoach AI</h2>
            <p>AI-powered fitness, diet & wellness platform</p>
            <p><b>Creators:</b> Navketan, Om, Vedant, Avishkar</p>
        </div>
        """, unsafe_allow_html=True)
