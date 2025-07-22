
import streamlit as st
import pandas as pd
from datetime import datetime
# from stripe_config import stripe
# Dashboard title
st.set_page_config(page_title="LucidEdge Dojo Dashboard", layout="wide")
st.title("LucidEdge Dojo Instructor Dashboard")

tabs = st.tabs(["Dropout Risk", "Promotion Eligibility", "Billing"])

# Dropout Risk Tab
with tabs[0]:
    st.header("📉 Dropout Risk Report")
    try:
        dropout_df = pd.read_csv("student_dropout_risk_corrected.csv")
        st.dataframe(dropout_df)
    except Exception as e:
        st.error(f"Failed to load dropout data: {e}")

# Promotion Eligibility Tab
with tabs[1]:
    st.header("🥋 Promotion Eligibility Tracker")
    try:
        promo_df = pd.read_csv("student_flexible_promotion_eligibility.csv")
        st.dataframe(promo_df)
    except Exception as e:
        st.error(f"Failed to load promotion data: {e}")

# Billing Tab
with tabs[2]:
    st.header("💳 Billing Management (Simulated)")

    with st.form("billing_form"):
        name = st.text_input("Student Name")
        email = st.text_input("Student Email")
        plan = st.selectbox("Plan", ["Basic - $49/mo", "Unlimited - $99/mo", "Private - $199/mo"])
        submitted = st.form_submit_button("Create Customer & Start Subscription")

        if submitted and name and email:
            st.success(f"Simulated: Created {name} on {plan}")

    if "customers" not in st.session_state:
        st.session_state["customers"] = []

    if submitted and name and email:
        st.session_state["customers"].append({
            "name": name,
            "email": email,
            "plan": plan,
            "start_date": datetime.now().strftime("%Y-%m-%d")
        })

    if st.session_state["customers"]:
        st.subheader("Current Simulated Subscriptions")
        st.dataframe(pd.DataFrame(st.session_state["customers"]))
