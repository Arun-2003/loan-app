import streamlit as st
import pandas as pd
from joblib import load

# Page config
st.set_page_config(
    page_title="Loan Prediction",
    page_icon="💰",
    layout="centered"
)

# Hide top header
st.markdown("""
    <style>
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #dbeafe 0%, #fce7f3 50%, #dcfce7 100%);
    }

    .main-title {
        text-align: center;
        color: #0f172a;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #334155;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1d4ed8;
        margin-bottom: 12px;
    }

    .stButton > button {
        width: 100%;
        height: 3.2em;
        border: none;
        border-radius: 14px;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        font-size: 17px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #6d28d9);
        color: white;
    }

    label {
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
model = load("model.joblib")
scaler = load("scaler.joblib")

# Title
st.markdown('<div class="main-title">💰 Loan Repayment Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Check if a borrower is likely to repay the loan</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Enter Borrower Details</div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])

with col2:
    applicant_income = st.number_input("Applicant Income (₹)", min_value=0, step=5000, format="%d")
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=5000, format="%d")
    loan_amount_rupees = st.number_input("Loan Amount (₹)", min_value=0, step=5000, format="%d")
    loan_term = st.number_input("Loan Term (months)", min_value=0, step=12, format="%d")
    credit_history_text = st.selectbox("Credit History", ["Good", "Bad"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Convert inputs
gender = 1 if gender == "Male" else 0
married = 1 if married == "Yes" else 0
education = 1 if education == "Graduate" else 0
self_employed = 1 if self_employed == "Yes" else 0
property_area = 2 if property_area == "Urban" else 1 if property_area == "Semiurban" else 0
dependents = 3 if dependents == "3+" else float(dependents)
credit_history = 1.0 if credit_history_text == "Good" else 0.0

# Fix loan scaling (VERY IMPORTANT)
loan_amount = loan_amount_rupees / 1000.0

# Create dataframe
input_data = pd.DataFrame([[
    gender, married, dependents, education, self_employed,
    applicant_income, coapplicant_income, loan_amount,
    loan_term, credit_history, property_area
]], columns=[
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
    "Loan_Amount_Term", "Credit_History", "Property_Area"
])

# Scale input
input_scaled = scaler.transform(input_data)

# Predict (FIXED LOGIC 🔥)
if st.button("🔍 Predict Repayment Status"):

    prob = model.predict_proba(input_scaled)[0][1]

    st.info(f"Repayment Probability: {prob:.2%}")

    # CUSTOM THRESHOLD (IMPORTANT)
    if prob > 0.35:
        st.success("✅ Loan will be Repaid")
    else:
        st.error("❌ Loan may Default")

    # Risk Level
    if prob > 0.7:
        st.success("🟢 Low Risk")
    elif prob > 0.4:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")