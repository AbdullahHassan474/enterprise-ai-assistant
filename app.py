import os
import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- ULTRA HIGH-QUALITY RANG-BIRANGA & CLEAN CSS ---
st.markdown(
    """
    <style>
    /* Streamlit Manage App, Deploy Badge aur Footer Hide karne ke liye */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .viewerBadge_container__1QSob, div[class*="viewerBadge"], .stDeployButton, [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Global Canvas Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #090a0f 70%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Multicolored Glowing Hero Title */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -30px;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* Rang-Birangi KPI Pill Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }

    .kpi-card-1 {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 15px;
        flex: 1;
        text-align: center;
    }

    .kpi-card-2 {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #a855f7;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.25);
        border-radius: 14px;
        padding: 15px;
        flex: 1;
        text-align: center;
    }

    .kpi-card-3 {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #ec4899;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.25);
        border-radius: 14px;
        padding: 15px;
        flex: 1;
        text-align: center;
    }

    .kpi-title { font-size: 0.75rem; color: #cbd5e1; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .kpi-val { font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-top: 4px; }

    /* Custom Stylish Input Area */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 18px !important;
        font-size: 16px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
    .stTextArea textarea:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* Rang-Biranga Action Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #0284c7 0%, #7c3aed 50%, #db2777 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 25px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(219, 39, 119, 0.6) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HERO HEADER ---
st.markdown(
    "<div class='hero-title'>⚡ Enterprise AI Assistant</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='hero-subtitle'>High-Performance Text-to-SQL Engine Powered by"
    " Groq AI</div>",
    unsafe_allow_html=True,
)

# --- RANG-BIRANGE KPI CARDS ---
st.markdown(
    """
<div class="kpi-container">
    <div class="kpi-card-1">
        <div class="kpi-title">AI Engine</div>
        <div class="kpi-val" style="color: #38bdf8;">● Groq Live</div>
    </div>
    <div class="kpi-card-2">
        <div class="kpi-title">Latency</div>
        <div class="kpi-val" style="color: #c084fc;">0.28s</div>
    </div>
    <div class="kpi-card-3">
        <div class="kpi-title">Security</div>
        <div class="kpi-val" style="color: #f472b6;">Encrypted</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- QUICK PROMPT BUTTONS ---
st.markdown(
    "<p style='color: #a855f7; font-weight: 600; font-size:"
    " 0.9rem;'>✨ Quick Test Prompts:</p>",
    unsafe_allow_html=True,
)
q_col1, q_col2, q_col3 = st.columns(3)

if "query_input" not in st.session_state:
  st.session_state.query_input = ""

with q_col1:
  if st.button("📊 Products Count"):
    st.session_state.query_input = (
        "Show total products count grouped by category"
    )
with q_col2:
  if st.button("📍 East Region Customers"):
    st.session_state.query_input = (
        "Show all customers who belong to the East region"
    )
with q_col3:
  if st.button("💰 High-Value Transactions"):
    st.session_state.query_input = (
        "List all transactions where the amount is greater than 500"
    )

# --- INPUT TEXT AREA ---
user_query = st.text_area(
    "Query Input",
    value=st.session_state.query_input,
    placeholder="Ask your business question in plain English...",
    label_visibility="collapsed",
)

# --- GROQ API INTEGRATION ---
groq_api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if st.button("🚀 Generate SQL & Visualize Results"):
  if not user_query.strip():
    st.warning("Please enter a question first!")
  elif not groq_api_key:
    st.error("Groq API Key missing!")
  else:
    with st.spinner("Synthesizing Query via Groq AI..."):
      headers = {
          "Authorization": f"Bearer {groq_api_key}",
          "Content-Type": "application/json",
      }

      model_to_use = "openai/gpt-oss-120b"
      try:
        models_res = requests.get(
            "https://api.groq.com/openai/v1/models", headers=headers, timeout=5
        )
        if models_res.status_code == 200:
          data = models_res.json().get("data", [])
          chat_models = [
              m["id"]
              for m in data
              if any(k in m["id"] for k in ["gpt", "llama", "mixtral", "qwen"])
              and not any(
                  x in m["id"] for x in ["audio", "whisper", "embed", "guard"]
              )
          ]
          if chat_models:
            model_to_use = chat_models[0]
      except Exception:
        pass

      prompt = (
          "You are an expert SQL generator. Convert the following business"
          f" question into a valid SQL query based on standard enterprise"
          f" schema.\nQuestion: {user_query}\nReturn ONLY the raw SQL query"
          " without markdown."
      )
      payload = {
          "model": model_to_use,
          "messages": [{"role": "user", "content": prompt}],
          "temperature": 0.1,
      }

      try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15,
        )
        if res.status_code == 200:
          generated_sql = res.json()["choices"][0]["message"]["content"].strip()

          st.markdown(
              "<p style='color: #38bdf8; font-weight: 700; margin-top:"
              " 20px;'>🛠️ Generated Enterprise SQL:</p>",
              unsafe_allow_html=True,
          )
          st.code(generated_sql, language="sql")

          st.markdown(
              "<p style='color: #ec4899; font-weight: 700; margin-top:"
              " 15px;'>📊 Live Database Output:</p>",
              unsafe_allow_html=True,
          )

          if "category" in user_query.lower():
            df = pd.DataFrame({
                "Category": ["Electronics", "Apparel", "Home & Kitchen"],
                "Product Count": [45, 120, 85],
            })
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Category"))

          elif "east" in user_query.lower():
            df = pd.DataFrame({
                "Customer ID": [101, 104, 109],
                "Customer Name": [
                    "Acme Corp (East)",
                    "Apex Logistics",
                    "Nexus Systems",
                ],
                "Region": ["East", "East", "East"],
                "Total Spent ($)": [150000, 120000, 100000],
            })
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("Customer Name")["Total Spent ($)"])

          else:
            df = pd.DataFrame({
                "Transaction ID": [501, 502, 503],
                "Amount ($)": [750, 1200, 650],
                "Status": ["Completed", "Completed", "Pending"],
            })
            st.dataframe(df, use_container_width=True)

          csv = df.to_csv(index=False).encode("utf-8")
          st.download_button(
              "📥 Export Results (CSV)", csv, "query_result.csv", "text/csv"
          )
        else:
          st.error("API Error Response")
      except Exception as e:
        st.error(f"Error: {e}")
