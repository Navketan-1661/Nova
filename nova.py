import streamlit as st
import pandas as pd
import sqlite3
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Nova FitCoach AI",
    layout="centered",
    page_icon="💪"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

/* Center login container */
.login-box {
    max-width: 420px;
    margin: 80px auto;
    background: #ffffff;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}

/* Title */
.login-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #1e3c72;
    margin-bottom: 20px;
}

/* Labels */
label {
    font-weight: 600 !important;
    color: #111827 !important;
}

/* Inputs */
input {
    background-color: #f9fafb !important;
    color: #111827 !important;
    border-radius: 10px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white;
    padding: 12px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e3a8a);
}
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
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

# ================= SESSION =================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("page", "Dashboard")

# ================= LOGIN SCREEN =================
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-box">
        <div class="login-title">Nova FitCoach AI</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN APP =================
else:
    with st.sidebar:
        st.markdown("## ☰ Menu")
        st.session_state.page = st.radio(
            "",
            ["Dashboard", "Fitness", "Diet", "Wellness", "Calculator", "Feedback", "About Us"]
        )

    if st.session_state.page == "Dashboard":
        st.markdown("""
        <div class="login-box">
            <h2>Welcome 👋</h2>
            <p>Your AI-powered fitness, diet & wellness assistant.</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.page == "Calculator":
        st.markdown("""
        <div class="login-box">
            <h2>📊 BMI Calculator</h2>
        """, unsafe_allow_html=True)

        weight = st.number_input("Weight (kg)", min_value=1.0)
        height = st.number_input("Height (cm)", min_value=1.0)

        if st.button("Calculate BMI"):
            bmi = weight / ((height / 100) ** 2)
            st.success(f"Your BMI is {bmi:.2f}")

        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "About Us":
        st.markdown("""
        <div class="login-box">
            <h2>About Nova FitCoach AI</h2>
            <p>AI-powered fitness, diet & mental wellness platform</p>
            <p><b>Team:</b> Navketan • Om • Vedant • Avishkar</p>
        </div>
        """, unsafe_allow_html=True)
