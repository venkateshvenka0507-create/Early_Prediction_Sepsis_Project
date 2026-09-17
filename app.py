import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sepsis Prediction", layout="wide")

st.title("🩺 Sepsis Prediction Dashboard")

# Load trained model
model = joblib.load("sepsis_model.pkl")

st.write("Enter patient data for 6 time steps")

data = []

# Input section
for i in range(6):
    st.subheader(f"Time Step {i+1}")
    
    hr = st.number_input(f"HR_{i}", 40, 180, 80)
    sbp = st.number_input(f"SBP_{i}", 80, 200, 120)
    temp = st.number_input(f"TEMP_{i}", 95.0, 105.0, 98.6)
    resp = st.number_input(f"RESP_{i}", 10, 40, 18)

    data.append([hr, sbp, temp, resp])

# Prediction button
if st.button("Predict Sepsis Risk"):

    # Flatten data (6×4 → 24 features)
    input_data = np.array(data).flatten().reshape(1, -1)

    prob = model.predict_proba(input_data)[0][1]

    st.subheader("Result")

    if prob < 0.3:
        st.success(f"LOW RISK ({prob:.2f})")
    elif prob < 0.7:
        st.warning(f"MEDIUM RISK ({prob:.2f})")
    else:
        st.error(f"HIGH RISK ({prob:.2f})")

    st.progress(float(prob))

    # Plot graph
    df = pd.DataFrame(data, columns=["HR", "SBP", "Temp", "Resp"])

    st.subheader("Patient Trend")
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    st.pyplot(fig)