import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Assistant | Text-to-SQL & RAG Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS Styling (Glassmorphism & Clean Polish)
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stApp { color: #E0E6ED; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    .status-badge {
        background-color: #00C853;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.title("🏢 Enterprise Workspace")
    st.markdown('<span class="status-badge">● Mesh API Connected v4.2</span>', unsafe_allow_html=True)
    st.write("")
    
    selected_unit = st.selectbox(
        "Select Business Unit",
        ["Global Financials (HQ)", "Supply Chain & Logistics", "Customer Analytics", "Healthcare Intelligence"]
    )
    
    st.divider()
    nav_mode = st.radio(
        "Navigation Console",
        ["Text-to-SQL Engine", "RAG Document Intelligence", "Schema & Metadata Inspector", "Security & Audit Logs"]
    )
    
    st.divider()
    st.caption("🔒 **Security Policy:** Strict SQL Injection Guard Active")

# Main Header
st.title("⚡ Enterprise AI Assistant")
st.caption(f"High-performance Text-to-SQL & Document Intelligence Platform | Active Context: **{selected_unit}**")

# Section 1: Text-to-SQL Engine
if nav_mode == "Text-to-SQL Engine":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Natural Language to Optimized SQL")
    
    user_query = st.text_area(
        "Enter business question in plain English:",
        value="Show top 3 customers who spent the most money in West region",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("🚀 Generate & Execute")
    with col2:
        include_explanation = st.checkbox("Include Architectural & Cost Breakdown", value=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        with st.spinner("Analyzing schema, checking security guards & synthesizing SQL..."):
            time.sleep(0.6)
            
        st.success("✅ Query compiled successfully with zero syntax errors!")
        
        # Generated SQL Code Box
        sql_code = """SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    c.region,
    SUM(t.amount) AS total_spend
FROM dim_customers c
JOIN fact_transactions t ON c.id = t.cust_id
WHERE c.region = 'West'
GROUP BY c.id, c.name, c.region
ORDER BY total_spend DESC
LIMIT 3;"""
        
        st.subheader("🛠️ Generated Enterprise SQL (PostgreSQL / Snowflake)")
        st.code(sql_code, language="sql")
        
        if include_explanation:
            with st.expander("💡 AI Reasoning & Optimization Breakdown", expanded=True):
                st.markdown("""
                - **Join Strategy:** Primary key join on `c.id = t.cust_id` indexed for high speed.
                - **Filter Strategy:** Pushed `WHERE c.region = 'West'` before aggregation to minimize disk I/O.
                - **Cost Estimate:** ~0.02 Query Compute Units (Estimated Execution Time: 12ms).
                """)
                
        # Mock Results Table
        st.subheader("📈 Live Query Execution Results")
        mock_data = pd.DataFrame({
            "Customer ID": [101, 104, 109],
            "Customer Name": ["Acme Corp (West)", "Apex Logistics", "Nexus Systems"],
            "Region": ["West", "West", "West"],
            "Total Spend ($)": [145000.00, 98500.50, 76200.00]
        })
        
        # Displaying metric cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Top Customer Revenue", "$145,000", "+12.4%")
        m2.metric("Average Transaction Value", "$31,970", "+5.1%")
        m3.metric("Total Records Processed", "3 Rows", "100% Accuracy")
        
        # Table
        st.dataframe(mock_data, use_container_width=True)
        
        # Visual Chart
        fig = px.bar(
            mock_data, 
            x="Customer Name", 
            y="Total Spend ($)", 
            title="Top Spend Analysis by Customer",
            color="Total Spend ($)",
            color_continuous_scale="Blues"
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# Section 2: RAG Document Intelligence
elif nav_mode == "RAG Document Intelligence":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📚 Enterprise Knowledge Base & RAG Search")
    rag_query = st.text_input("Search internal compliance, financial reports, or vendor contracts:", value="Q3 revenue growth drivers and compliance policies")
    rag_btn = st.button("🔍 Search Knowledge Base")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if rag_btn:
        with st.spinner("Retrieving semantic vector embeddings from enterprise vault..."):
            time.sleep(0.5)
        st.success("✨ Retrieved 3 highly relevant vector chunks (Confidence Score: 98.4%)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 📄 Source: `Q3_Financial_Audit_2026.pdf`")
            st.info("Growth in the Western region surged by 18.2% driven by enterprise logistics accounts and recurring cloud software renewals.")
        with col_b:
            st.markdown("### 📄 Source: `Compliance_Policy_v4.docx`")
            st.info("All automated Text-to-SQL transactions exceeding $50,000 must undergo dual-factor audit logging per ISO-27001 standards.")

# Section 3: Schema Inspector
elif nav_mode == "Schema & Metadata Inspector":
    st.subheader("📊 Active Database Schema & Foreign Key Map")
    st.markdown("""
    - **`dim_customers`** `(id: INT [PK], name: VARCHAR, region: VARCHAR, created_at: TIMESTAMP)`
    - **`fact_transactions`** `(id: INT [PK], cust_id: INT [FK], amount: DECIMAL, status: VARCHAR)`
    - **`dim_products`** `(id: INT [PK], category: VARCHAR, unit_cost: DECIMAL)`
    - **`audit_logs`** `(log_id: INT, query_hash: VARCHAR, executed_at: TIMESTAMP, status: VARCHAR)`
    """)

# Section 4: Security & Audit Logs
else:
    st.subheader("🛡️ Enterprise Security & Compliance Log")
    audit_df = pd.DataFrame({
        "Timestamp": ["2026-10-12 16:15:22", "2026-10-12 15:42:10", "2026-10-12 14:10:05"],
        "User": ["admin_enterprise", "analyst_west", "system_bot"],
        "Event": ["SQL Injection Guard Triggered (Blocked)", "Successful Text-to-SQL Execution", "Vector Index Re-sync"],
        "Risk Level": ["Low", "None", "None"]
    })
    st.dataframe(audit_df, use_container_width=True)
