import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_financial_data
from risk_score import RiskScoringEngine
import joblib
import os
import io

st.set_page_config(page_title="FinSafe - Fraud Monitoring Dashboard", layout="wide")

st.title("💷 FinSafe: Financial Fraud Detection & Risk Scoring")
st.markdown("Real-time monitoring and risk analysis for Nigerian Financial Transactions.")

# 1. Sidebar - Configuration
st.sidebar.header("Data Sources")
data_option = st.sidebar.selectbox("Select Data Source", ["Synthetic Data", "Real Data (Subset)"])
btn_load = st.sidebar.button("Load Data")

st.sidebar.divider()
st.sidebar.header("Export Data")
if 'df' in st.session_state:
    # Convert to Excel in memory
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        st.session_state.df.to_excel(writer, index=False, sheet_name='FraudData')
    
    st.sidebar.download_button(
        label="📥 Download as Excel",
        data=buffer.getvalue(),
        file_name="fraud_monitoring_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.sidebar.info("Load data first to enable Excel export.")

# 2. Main Dashboard Logic
@st.cache_data
def get_dashboard_data(source):
    if source == "Synthetic Data":
        return load_financial_data(limit=5000, use_synthetic=True)
    else:
        # For Real Data, strictly use streaming to avoid symlink/download errors
        return load_financial_data(limit=5000, use_synthetic=False)

if btn_load or 'df' in st.session_state:
    if btn_load:
        st.session_state.df = get_dashboard_data(data_option)
    
    df = st.session_state.df
    
    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    total_txns = len(df)
    # Detect fraud col (handling different schemas)
    fraud_col = 'is_fraud' if 'is_fraud' in df.columns else 'isFraud'
    amt_col = 'amount_ngn' if 'amount_ngn' in df.columns else 'amount'
    
    fraud_count = df[fraud_col].astype(int).sum()
    fraud_rate = (fraud_count / total_txns) * 100
    total_volume = df[amt_col].sum()
    
    kpi1.metric("Total Transactions", f"{total_txns:,}")
    kpi2.metric("Fraud Rate", f"{fraud_rate:.2f}%")
    kpi3.metric("Total Volume (NGN)", f"{total_volume:,.2f}")

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Type Distribution")
        fig_type = px.pie(df, names='transaction_type' if 'transaction_type' in df.columns else 'type', 
                        title="Volume by Type", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_type, use_container_width=True)
        
    with col2:
        st.subheader("Fraud by Category")
        if 'merchant_category' in df.columns:
            cat_df = df.groupby('merchant_category')[fraud_col].sum().reset_index()
            fig_cat = px.bar(cat_df, x='merchant_category', y=fraud_col, title="Fraud Counts per Category",
                             color_discrete_sequence=['#FF4B4B'])
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Category data not available for this data source.")

    # Risk Scoring Tool
    st.divider()
    st.header("🔍 Individual Transaction Risk Scorer")
    
    with st.expander("Evaluate a Custom Transaction"):
        t_col1, t_col2, t_col3 = st.columns(3)
        t_amt = t_col1.number_input("Transaction Amount (NGN)", min_value=0.0, value=50000.0)
        t_type = t_col2.selectbox("Type", df['transaction_type'].unique() if 'transaction_type' in df.columns else ['TRANSFER', 'PAYMENT', 'CASH_OUT'])
        t_loc = t_col3.text_input("Location", "Lagos, Nigeria")
        
        if st.button("Calculate Risk Score"):
            engine = RiskScoringEngine()
            score = engine.calculate_risk_score({'amount': t_amt, 'transaction_type': t_type})
            
            # Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Transaction Risk Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#FF4B4B" if score > 70 else "#FFA500" if score > 40 else "#00CC96"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "gray"}],
                }
            ))
            st.plotly_chart(fig_gauge)
            
            if score > 70:
                st.error("🚨 HIGH RISK: Transaction flagged for manual review.")
            elif score > 40:
                st.warning("⚠️ MEDIUM RISK: Monitor this account for further activity.")
            else:
                st.success("✅ LOW RISK: Transaction appears legitimate.")

    # Data Preview
    st.divider()
    st.subheader("Recent Transactions")
    st.dataframe(df.head(20), use_container_width=True)

else:
    st.info("Click 'Load Data' in the sidebar to begin monitoring.")
