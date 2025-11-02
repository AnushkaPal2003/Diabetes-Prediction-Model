import streamlit as st
import numpy as np
import pandas as pd
from joblib import load

# Load model
model = load(open('xgboost.joblib', 'rb'))

# Page config
st.set_page_config(page_title="Diabetes Risk Predictor", layout="centered")
st.title("🩺 Diabetes Risk Prediction App")
st.markdown("Tool to assess diabetes risk based on key health indicators.")

# Sidebar inputs
st.sidebar.header("📋 Enter Patient Details")

pregnancies = st.sidebar.number_input("Pregnancies", min_value=0, max_value=20, value=2, help="Number of times pregnant")
glucose = st.sidebar.number_input("Glucose Level", min_value=0, max_value=200, value=120, help="Plasma glucose concentration")
bp = st.sidebar.number_input("Blood Pressure", min_value=0, max_value=180, value=70, help="Diastolic blood pressure (mm Hg)")
skin = st.sidebar.number_input("Skin Thickness", min_value=0, max_value=100, value=20, help="Triceps skin fold thickness (mm)")
insulin = st.sidebar.number_input("Insulin", min_value=0, max_value=900, value=85, help="2-Hour serum insulin (mu U/ml)")
bmi = st.sidebar.number_input("BMI", min_value=0.0, max_value=60.0, value=25.0, help="Body Mass Index")
dpf = st.sidebar.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5, help="Genetic risk factor")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=33, help="Age in years")

# Predict button
if st.button("🔍 Predict Diabetes Risk"):
    input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
    prediction = model.predict(input_data)[0]

    st.subheader("🧠 Prediction Result")
    if prediction == 1:
        st.error("⚠️ The model predicts **Diabetic**. Please consult a healthcare professional.")
    else:
        st.success("✅ The model predicts **Non-Diabetic**. Keep up the healthy lifestyle!")

# Expandable info section
with st.expander("📖 Click to learn what each feature means"):
    st.markdown("""
    - **Pregnancies**: Number of times the patient has been pregnant.
    - **Glucose**: Plasma glucose concentration after fasting.
    - **Blood Pressure**: Diastolic blood pressure in mm Hg.
    - **Skin Thickness**: Triceps skin fold thickness.
    - **Insulin**: 2-hour serum insulin level.
    - **BMI**: Body Mass Index (weight/height²).
    - **Diabetes Pedigree Function**: Likelihood of diabetes based on family history.
    - **Age**: Patient's age in years.
            
    """)

# Ask for patient name
name = st.text_input("👤 Patient Name")


# Reference ranges
reference = {
    "Pregnancies": "0–6",
    "Glucose": "< 140 mg/dL",
    "Blood Pressure": "< 80 mm Hg",
    "Skin Thickness": "~20 mm",
    "Insulin": "< 100 µU/mL",
    "BMI": "< 25",
    "Diabetes Pedigree Function": "< 1.0",
    "Age": "18–45 (low risk)"
}

# Show report table
if st.button("📄 Generate Medical Report"):
    name
    report_data = {
        "Feature": ["Age", "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "Diabetes Pedigree Function"],
        "Your Value": [age, pregnancies, glucose, bp, skin, insulin, bmi, dpf],
        "Normal Range": [reference["Age"], reference["Pregnancies"], reference["Glucose"], reference["Blood Pressure"],
                         reference["Skin Thickness"], reference["Insulin"], reference["BMI"], reference["Diabetes Pedigree Function"]]
    }

    report_df = pd.DataFrame(report_data)
    st.subheader("🧾 Patient Report Summary")
    st.table(report_df)

    # ✅ Convert to CSV from DataFrame
    csv = report_df.to_csv(index=False).encode('utf-8')

    # ✅ Download button
    st.download_button(
        label="⬇️ Download Report",
        data=csv,
        file_name=f"{name}_diabetes_report.csv",
        mime='text/csv'
    )

    # Footer
st.markdown("---")
st.caption("Built with ❤️ by Anushka Pal")