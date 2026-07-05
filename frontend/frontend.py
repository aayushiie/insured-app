import streamlit as st
import requests

st.set_page_config(
    page_title="Insurance Predictor",
    page_icon="🌸",
    layout="wide"
)

API_URL = "http://204.236.253.180:8000/predict"

st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; }
    [.stButton>button] { width: 100%; border-radius: 8px; font-weight: bold; }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #e9ecef;
    }
    .card h3 { color: #6c757d; font-size: 14px; margin-bottom: 5px; }
    .card h1 { color: #1e3a8a; font-size: 32px; margin: 0; }
    </style>
""", unsafe_allow_html=True)

st.title("Medical Insurance Category Predictor")
st.markdown("Provide client metrics below to generate a real-time risk tier prediction.")

st.sidebar.header("Demographics")
age = st.sidebar.number_input("Age", min_value=1, max_value=119, value=30)
gender = st.sidebar.selectbox("Gender", options=['male', 'female'])
region = st.sidebar.selectbox('Region', options=['northeast', 'northwest', 'southeast', 'southwest'])
num_children = st.sidebar.number_input("Number of Children", min_value=0, value=1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical & Risk Profiling")
    weight = st.number_input("Weight (kg)", min_value=0.1, value=65.0)
    height = st.number_input("Height (m)", min_value=0.1, max_value=2.5, value=1.7)
    smokes = st.selectbox('Smoker Status', options=['yes', 'no'])
    risk_score = st.number_input("Risk Score", min_value=0.01, max_value=8.99, value=5.45)
    is_high_risk = st.selectbox("High Risk Flag", options=[True, False])

with col2:
    st.subheader("Financial & Interaction Tracking")
    charges = st.number_input("Total Charges ($)", min_value=0.01, value=1789.8)
    monthly_premium_est = st.number_input("Estimated Monthly Premium ($)", min_value=0.01, value=1506.9)
    charges_per_child = st.number_input("Charges Per Child ($)", min_value=0.01, value=156.8)
    bmi_age_interaction = st.number_input("BMI-Age Interaction Factor", min_value=0.01, value=749.8)

st.markdown("---")

if st.button("Generate Categorization Report", type="primary"):
    payload = {
        "age": int(age),
        "gender": gender,
        "weight": float(weight),
        "height": float(height),
        "smokes": smokes,
        "region": region,
        "charges": float(charges),
        "monthly_premium_est": float(monthly_premium_est),
        "charges_per_child": float(charges_per_child),
        "bmi_age_interaction": float(bmi_age_interaction),
        "risk_score": float(risk_score),
        "is_high_risk": bool(is_high_risk),
        "num_children": int(num_children)
    }
    
    try:
        with st.spinner("Streaming metrics to engine..."):
            response = requests.post(API_URL, json=payload)
            
        if response.status_code == 200:
            raw_data = response.json()
            
            prediction_payload = raw_data.get('predicted_category', {})
            category = prediction_payload.get('predicted_category', 'N/A')
            confidence = prediction_payload.get('confidence', 0.0)
            probabilities = prediction_payload.get('class_probabilities', {})
            
            st.subheader("Analytical Predictions")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown(f"<div class='card'><h3>Assigned Tier</h3><h1>{category}</h1></div>", unsafe_allow_html=True)
            with res_col2:
                st.markdown(f"<div class='card'><h3>Model Certainty</h3><h1>{confidence * 100:.2f}%</h1></div>", unsafe_allow_html=True)
            
            if probabilities:
                st.markdown("### Class Probability Distribution")
                sorted_probs = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
                
                for tier, prob in sorted_probs:
                    col_label, col_bar = st.columns([1, 4])
                    with col_label:
                        st.markdown(f"**{tier}** ({prob * 100:.1f}%)")
                    with col_bar:
                        st.progress(float(prob))
        else:
            st.error(f"Backend Server Rejection ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Connection Failed. Verify the FastAPI deployment is running locally on port 8000.")
