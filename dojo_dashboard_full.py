
import pandas as pd
import streamlit as st
import uuid

from stripe_config import STRIPE_SECRET_KEY, STRIPE_PRICE_ID

# Load data
attendance_df = pd.read_csv("attendance_with_names.csv")
dropout_df = pd.read_csv("student_dropout_risk_corrected.csv")
eligibility_df = pd.read_csv("student_flexible_promotion_eligibility.csv")

# Initialize billing customers
if "customers" not in st.session_state:
    st.session_state.customers = []

st.set_page_config(page_title="DojoFlow Dashboard", layout="wide")
st.title("🏆 DojoFlow AI Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["📉 Dropout Risk", "🥋 Promotion Eligibility", "💳 Billing"])

with tab1:
    st.subheader("📉 Dropout Risk")
    at_risk = dropout_df[dropout_df['at_risk']]
    st.dataframe(at_risk[['student_id', 'name', 'days_since_last_class']], use_container_width=True)

with tab2:
    st.subheader("🥋 Promotion Eligibility")
    eligible = eligibility_df[eligibility_df['eligible_for_promotion']]
    st.dataframe(eligible[['student_id', 'name', 'belt_rank', 'classes_attended', 'days_since_join']], use_container_width=True)

    st.subheader("📊 All Students Summary")
    st.dataframe(eligibility_df, use_container_width=True)

with tab3:
    st.subheader("➕ Add New Student to Billing")
    with st.form("add_customer"):
        name = st.text_input("Student Name")
        email = st.text_input("Student Email")
        plan = st.selectbox("Select Plan", ["Basic Monthly ($99)", "Advanced Monthly ($149)"])
        submitted = st.form_submit_button("Create Customer & Start Subscription")
        if submitted:
            customer_id = f"cus_{uuid.uuid4().hex[:8]}"
            subscription_id = f"sub_{uuid.uuid4().hex[:8]}"
            st.session_state.customers.append({
                "name": name,
                "email": email,
                "plan": plan,
                "customer_id": customer_id,
                "subscription_id": subscription_id,
                "status": "active"
            })
            st.success(f"✅ Created subscription for {name} ({email}) on {plan}")

    st.subheader("📋 Current Subscriptions")
    df = pd.DataFrame(st.session_state.customers)
    if not df.empty:
        st.dataframe(df[["name", "email", "plan", "status"]], use_container_width=True)
    else:
        st.info("No subscriptions created yet.")
