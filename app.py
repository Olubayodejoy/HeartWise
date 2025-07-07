import streamlit as st 
import numpy as np
import joblib

# Load models
model = joblib.load("heart_model.pkl")
risk_model = joblib.load("heart_risk_model.pkl")

# App setup
st.set_page_config(page_title="Heart Disease Risk Checker", layout="centered")

st.markdown("""
    <style>
        /* Page background and default text */
        .stApp {
            background-color: #FFF9C4;
            color: #000000 !important;
        }

        html, body, [class*="css"] {
            color: #000000 !important;
            background-color: #FFF9C4 !important;
        }

        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #000000 !important;
        }

        /* Input fields, select boxes, sliders, etc. */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input,
        .stSlider > div,
        .stButton > button,
        .stRadio > div,
        .stTextArea > div > textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Column/box backgrounds */
        .block-container,
        .css-1v0mbdj, .css-12w0qpk {
            background-color: #FFF9C4 !important;
        }
    </style>
""", unsafe_allow_html=True)



st.title("💓 Welcome to HeartWise: Your Heart Health Predictor")

# Session state to manage page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Home Page
def show_home():
    st.subheader("🫀 What would you like to do?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💉 Check if you HAVE Heart Disease"):
            st.session_state.page = "detect"
    with col2:
        if st.button("⚠️ Check if you are AT RISK of Heart Disease"):
            st.session_state.page = "risk"

# Detection Page
def show_detection():
    st.header("💉 Heart Disease Detection")
    st.write("Fill in your medical details to check if you currently have heart disease.")

    age = st.number_input("Age", 1, 120, 30)
    sex = st.selectbox("Sex", ["Male", "Female"])
    resting_bp = st.number_input("Resting BP", 60, 200, 120)
    cholesterol = st.number_input("Cholesterol", 100, 400, 180)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl?", ["No", "Yes"])
    max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["No", "Yes"])
    oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, step=0.1)
    cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
    ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
    slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    # Encoding
    sex = 1 if sex == "Male" else 0
    fasting_bs = 1 if fasting_bs == "Yes" else 0
    exercise_angina = 1 if exercise_angina == "Yes" else 0
    cp_ATA = 1 if cp == "Atypical Angina" else 0
    cp_NAP = 1 if cp == "Non-Anginal Pain" else 0
    cp_TA = 1 if cp == "Typical Angina" else 0
    ecg_normal = 1 if ecg == "Normal" else 0
    ecg_st = 1 if ecg == "ST" else 0
    slope_flat = 1 if slope == "Flat" else 0
    slope_up = 1 if slope == "Up" else 0

    features = np.array([[age, sex, resting_bp, cholesterol, fasting_bs, max_hr,
                          exercise_angina, oldpeak,
                          cp_ATA, cp_NAP, cp_TA,
                          ecg_normal, ecg_st,
                          slope_flat, slope_up]])

    if st.button("🩺 Predict Now"):
        pred = model.predict(features)[0]
        if pred == 1:
            st.error("🚨 You may currently have heart disease.")
            st.markdown("### Care Tips If You Have Heart Disease:")
            st.markdown("- **See a cardiologist** immediately.")
            st.markdown("- **Cut down on salt and fried food.**")
            st.markdown("- **Engage in light exercises (if approved).**")
            st.markdown("- **Stick to your medications.**")
            st.markdown("- **Reduce stress with yoga or breathing.**")
        else:
            st.success("✅ You are not currently showing signs of heart disease.")
            st.markdown("### Keep Living Healthy:")
            st.markdown("- Maintain a balanced diet.")
            st.markdown("- Stay active regularly.")
            st.markdown("- Stay hydrated and rest well.")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

# Risk Estimator Page
def show_risk():
    st.header("⚠️ Heart Disease Risk Estimator")
    st.write("Check your lifestyle-based risk of developing heart disease.")

    age = st.number_input("Age", 10, 100, 30)
    sex = st.selectbox("Sex", ["Male", "Female"])
    smoker = st.selectbox("Do you smoke?", ["Yes", "No"])
    exercise = st.slider("Exercise days/week", 0, 7, 3)
    diet = st.selectbox("Diet quality", ["Good", "Poor"])
    family = st.selectbox("Family History", ["Yes", "No"])
    stress = st.selectbox("Stress Level", ["Low", "Moderate", "High"])
    sleep = st.slider("Sleep hours", 3, 10, 6)

    features = {
        "Age": age,
        "ExercisePerWeek": exercise,
        "SleepHours": sleep,
        "Sex_Male": 1 if sex == "Male" else 0,
        "Smoker_Yes": 1 if smoker == "Yes" else 0,
        "Diet_Poor": 1 if diet == "Poor" else 0,
        "FamilyHistory_Yes": 1 if family == "Yes" else 0,
        "Stress_Moderate": 1 if stress == "Moderate" else 0,
        "Stress_High": 1 if stress == "High" else 0,
    }

    X = np.array([list(features.values())])

    if st.button("🧠 Estimate Risk"):
        pred = risk_model.predict(X)[0]
        if pred == 1:
            st.error("⚠️ You may be at high risk of developing heart disease.")
            st.markdown("### Prevention Tips:")
            st.markdown("- **Quit smoking immediately.**")
            st.markdown("- **Exercise 30 min/day.**")
            st.markdown("- **Improve your diet (fiber, fish, grains).**")
            st.markdown("- **Reduce stress regularly.**")
            st.markdown("- **Sleep at least 7–8 hours.**")
        else:
            st.success("✅ Your risk level is low. Well done!")
            st.markdown("### Keep it up:")
            st.markdown("- Maintain your healthy habits.")
            st.markdown("- Stay physically active.")
            st.markdown("- Drink water and manage stress.")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

# Page router
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "detect":
    show_detection()
elif st.session_state.page == "risk":
    show_risk()
