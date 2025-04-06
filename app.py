import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("diabetes_model.pkl")

st.title("🩺 Diabetes Readmission Prediction App")
st.markdown("Enter patient details to predict the risk of readmission.")

# Input form
with st.form("prediction_form"):
    race = st.selectbox("Race", ['Caucasian', 'AfricanAmerican', 'Hispanic', 'Asian', 'Other'])
    gender = st.selectbox("Gender", ['Male', 'Female'])
    age = st.selectbox("Age", ['[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)'])
    time_in_hospital = st.number_input("Time in Hospital (days)", 1, 14)
    num_medications = st.slider("Number of Medications", 1, 50, 10)
    num_procedures = st.slider("Number of Procedures", 0, 6, 1)
    change = st.selectbox("Change in Medications?", ['No', 'Ch'])
    diabetesMed = st.selectbox("Diabetes Medication Prescribed?", ['Yes', 'No'])

    submit = st.form_submit_button("Predict")

if submit:
    # Prepare input
    input_data = pd.DataFrame({
        'race': [race],
        'gender': [gender],
        'age': [age],
        'time_in_hospital': [time_in_hospital],
        'num_medications': [num_medications],
        'num_procedures': [num_procedures],
        'change': [change],
        'diabetesMed': [diabetesMed],
    })

    # Match model columns
    input_encoded = pd.get_dummies(input_data)
    model_input = pd.DataFrame(columns=model.feature_names_in_)
    model_input = model_input.append(input_encoded, ignore_index=True).fillna(0)

    # Predict
    prediction = model.predict(model_input)[0]

    if prediction == 1:
        st.error("⚠️ The patient is likely to be readmitted.")
    else:
        st.success("✅ The patient is not likely to be readmitted.")
