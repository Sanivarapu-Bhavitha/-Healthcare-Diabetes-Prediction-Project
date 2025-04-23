import streamlit as st
import pickle 

# Load the trained model
with open('final_model.pkl', 'rb') as file:
    model = pickle.load(file)

def prediction(input_data):
    pred = model.predict(input_data)[0]
    return 'High Risk of Readmission' if pred == 1 else 'Low Risk of Readmission'

def get_age_group(age):
    if age < 10: return 1
    elif age < 20: return 2
    elif age < 30: return 3
    elif age < 40: return 4
    elif age < 50: return 5
    elif age < 60: return 6
    elif age < 70: return 7
    elif age < 80: return 8
    elif age < 90: return 9
    else: return 10

def main():
    st.title('Early Readmission Prediction for Diabetic Patients')
    st.subheader('Predicts whether a diabetic patient is at high risk of early hospital readmission.')
    
    st.markdown('### Input Patient Data')

    gender = st.radio('Gender (0: Male, 1: Female)', [0, 1], horizontal=True)
    age_input = st.number_input('Age', min_value=0, max_value=100, step=1)
    age = get_age_group(age_input)

    admission_type_id = st.selectbox(
        'Admission Type (1: Emergency, 2: Urgent, 3: Elective, etc.)',
        [1, 2, 3, 4, 5, 6, 7, 8]
    )
    
    time_in_hospital = st.number_input('Time in Hospital (Days)', min_value=1, max_value=30, step=1)
    num_lab_procedures = st.number_input('Number of Lab Procedures', min_value=0, step=1)
    num_medications = st.number_input('Number of Medications', min_value=0, step=1)
    number_inpatient = st.number_input('Number of Inpatient Visits', min_value=0, step=1)
    
    diag_1 = st.number_input('Primary Diagnosis Code', step=1)
    diag_2 = st.number_input('Secondary Diagnosis Code', step=1)
    diag_3 = st.number_input('Additional Diagnosis Code', step=1)

    metformin = st.radio('Metformin Use (0: No, 1: Yes)', [0, 1], horizontal=True)

    insulin_options = {
        0: 'No',
        1: 'Up',
        2: 'Steady',
        3: 'Down'
    }
    insulin_label = st.radio('Insulin Use', list(insulin_options.values()), horizontal=True)
    insulin = [k for k, v in insulin_options.items() if v == insulin_label][0]

    change = st.radio('Change in Medications (0: No, 1: Yes)', [0, 1], horizontal=True)
    diabetesMed = st.radio('Diabetes Medication (0: No, 1: Yes)', [0, 1], horizontal=True)

    discharged_to = st.number_input('Discharge Destination Code', min_value=1, max_value=30, step=1)

    input_list = [[
        float(gender), float(age), float(admission_type_id), float(time_in_hospital),
        float(num_lab_procedures), float(num_medications), float(number_inpatient),
        float(diag_1), float(diag_2), float(diag_3), float(metformin),
        float(insulin), float(change), float(diabetesMed), float(discharged_to)
    ]]

    if st.button('Predict'):
        result = prediction(input_list)
        st.success(result)

if __name__ == '__main__':
    main()
