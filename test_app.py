import streamlit as st
from joblib import load

st.title("Joblib Test App")

try:
    st.write("Trying to load joblib...")
    model = load("xgboost.joblib")
    st.success("✅ joblib loaded successfully!")
except Exception as e:
    st.error(f"❌ joblib failed: {e}")