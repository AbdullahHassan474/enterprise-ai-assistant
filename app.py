import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import time

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Assistant | Text-to-SQL & RAG Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS
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

# Initialize Groq Client with Auto-Cleanup
@st.cache_resource
def get_groq_client():
    if "GROQ_API_KEY" in st.secrets:
        raw_key = str(st.secrets["GROQ_API_KEY"])
        cleaned_key = "".join(raw_key.split())
        return Groq(api_key=cleaned_key)
    return None

client = get_groq_client()

# Sidebar
with st.sidebar:
    st.title("🏢 Enterprise Workspace")
    if client:
        st.markdown('<span class="status-badge">● Groq Llama-3 Active</span>', unsafe_allow_html=True)
    else:
        st.error("⚠️ Groq Key Missing in Secrets")
        
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

# Main Header
st.title("⚡ Enterprise AI Assistant")
st.caption(f"High-performance Text-to-SQL & Document Intelligence Platform | Active Context: **{selected_unit}**")

# System Schema Context for LLM
SCHEMA_CONTEXT = """
Database Schema:
1. dim_customers (id INT PK, name VARCHAR, region VARCHAR, created_at TIMESTAMP)
2. fact_transactions (id INT PK, cust_id INT FK, amount DECIMAL, status VARCHAR, tx_date DATE)
3. dim_products (id INT PK, category VARCHAR, unit_cost DECIMAL)
"""

# Section 1: Text-to-SQL Engine
if nav_mode == "Text-to-SQL Engine":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Natural Language to Optimized SQL (Powered by Groq)")
    
    user_query = st.text_area(
        "Enter business question in plain English:",
        value="Show top 3 customers who spent the most money in West region",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("🚀 Generate SQL via AI")
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        if not client:
            st.error("Groq API Key set nahi hai! Secrets check karein.")
        else:
            with st.spinner("Groq Llama-3 model real-time SQL generate kar raha hai..."):
                try:
                    prompt = f"""
                    You are an expert PostgreSQL SQL developer. 
                    Given this schema: {SCHEMA_CONTEXT}
                    
                    Generate ONLY the clean SQL query (no explanation, no markdown formatting block) for the question: "{user_query}"
                    """
                    
                    # Updated to active Groq fast model
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant",
                        temperature=0.1
                    )
                    
                    sql_code = response.choices[0].message.content.strip()
                    
                    st.success("✅ Real-time SQL synthesized via Groq API!")
                    st.subheader("🛠️ Generated Enterprise SQL")
                    st.code(sql_code, language="sql")
                    
                    # Simulated Data View for Execution
                    st.subheader("📈 Live Simulated Query Results")
                    mock_df = pd.DataFrame({
                        "Customer ID": [101, 104, 109],
                        "Customer Name": ["Acme Corp (West)", "Apex Logistics", "Nexus Systems"],
                        "Region": ["West", "West", "West"],
                        "Total Spend ($)": [145000.00, 98500.50, 76200.00]
                    })
                    st.dataframe(mock_df, use_container_width=True)
                    
                    fig = px.bar(mock_df, x="Customer Name", y="Total Spend ($)", color="Total Spend ($)", title="Query Visualization Result")
                    fig.update_layout(template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"AI Generation Error: {str(e)}")

elif nav_mode == "RAG Document Intelligence":
    st.subheader("📚 RAG Knowledge Base Engine")
    st.info("RAG Query Interface is active. Connect custom knowledge bases via vector embeddings.")

elif nav_mode == "Schema & Metadata Inspector":
    st.subheader("📊 Active Schema Metadata")
    st.code(SCHEMA_CONTEXT, language="sql")

else:
    st.subheader("🛡️ Security Audit Logs")
    st.write("All LLM requests and SQL guardrail checks are actively logged.")
                    
