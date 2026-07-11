import numpy as np
from PIL import Image
import streamlit as st

from backend.auth import signup, login
from backend.prediction import predict_quality
from backend.recommendation import recommend, explain_prediction
from backend.save_prediction import save_prediction

# =============================================
#  THEME INJECTION  (only addition)
# =============================================
import os

def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external stylesheet sitting next to app.py
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    load_css(css_path)
# =============================================




# ---------------- IMAGE FUNCTION ----------------
def analyze_image(image):

    img = np.array(image)

    avg_color = img.mean(axis=(0,1))
    brightness = img.mean()

    r, g, b = avg_color

    # -------- COLOR DETECTION --------
    if r > 150 and g > 100:
        color = "Light Brown"
    elif r > 100:
        color = "Brown"
    else:
        color = "Dark Brown"

    # -------- IMPURITY ESTIMATION --------
    if brightness > 180:
        impurity = "Low"
    elif brightness > 120:
        impurity = "Medium"
    else:
        impurity = "High"

    return color, impurity


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

menu = ["Login", "Signup"]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- SIGNUP ----------------
if choice == "Signup":

    st.title("Signup")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        signup(username, email, password)
        st.success("Account created successfully")


# ---------------- LOGIN ----------------
elif choice == "Login":

    if not st.session_state.logged_in:

        st.title("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Login successful")

            else:
                st.error("Invalid login")

    # ---------------- AFTER LOGIN ----------------
    if st.session_state.logged_in:

        st.title("Waste2Worth - Bagasse Quality Checker")

        st.subheader("Enter Bagasse Parameters")

        # ---------------- IMAGE INPUT ----------------
        uploaded_file = st.file_uploader("Upload Bagasse Image", type=["jpg","png","jpeg"])

        # default values
        color = "Brown"
        impurity = "Medium"

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Image")

            color, impurity = analyze_image(image)

            st.success(f"Detected Color: {color}")
            st.success(f"Estimated Impurity: {impurity}")

        # ---------------- INPUTS ----------------
        moisture = st.number_input("Moisture Content")
        fiber = st.number_input("Fiber Quality")

        # ❌ Removed manual impurity (now from image)
        odor = st.selectbox("Odor", ["Normal","Slight","Bad"])

        storage = st.number_input("Storage Days")

        # ---------------- PREDICTION ----------------
        if st.button("Check Quality"):

            impurity_map = {"Low":0,"Medium":1,"High":2}
            color_map = {"Light Brown":0,"Brown":1,"Dark Brown":2}
            odor_map = {"Normal":0,"Slight":1,"Bad":2}

            data = [
                moisture,
                fiber,
                impurity_map[impurity],
                color_map[color],
                odor_map[odor],
                storage
            ]

            # ML Prediction
            quality = predict_quality(data)

            # Recommendation
            result = recommend(quality)

            st.success(result)

            # Save to database
            save_prediction(
                st.session_state.email,
                moisture,
                fiber,
                impurity,
                color,
                odor,
                storage,
                result
            )

            # Explainable AI
            reasons = explain_prediction(moisture, fiber, impurity, odor)

            st.subheader("Prediction Explanation")

            for r in reasons:
                st.write("•", r)

        # ---------------- LOGOUT ----------------
        if st.button("Logout"):
            st.session_state.logged_in = False