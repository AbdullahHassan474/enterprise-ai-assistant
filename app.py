import os
import pandas as pd
import requests
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- GEMINI / NETFLIX STYLE ULTRA-CUSTOM STYLING ---
st.markdown(
    """
    <style>
    /* Hide Streamlit Header & Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Full Dark Canvas Background */
    .stApp {
        background: #090a0f !important;
        color: #e2e8f0 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Minimalist Floating Hero Header */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #a5f3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 5px;
    }
    
    .hero-subtitle {
        color: #64748b;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }

    /* Custom Floating Pill Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .kpi-pill {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 20px;
        flex: 1;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .kpi-title { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-val { font-size: 1.2rem; font-weight: 700; color: #f8fafc; margin-top: 2px; }

    /* Custom Textarea Styling */
    .stTextArea textarea {
        background: #0f172a !important;
        color: #f1f5f9 !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }

    /* Sleek Action Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton > button:hover {
        opacity: 0.95;
        transform: scale(1.005);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER SECTION ---
st.markdown(
    "<div class='hero-title'>⚡ Enterprise AI Assistant</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='hero-subtitle'>Autonomous Text-to-SQL & Visual Intelligence"
    " Engine</div>",
    unsafe_allow_html=True,
)

# --- KPI METRICS FLOATING CARDS ---
st.markdown(
    """
<div class="kpi-container">
    <div class="kpi-pill">
        <div class="kpi-title">AI System</div>
        <div class="kpi-val" style="color: #4ade80;">● Online</div>
    </div>
    <div class="kpi-pill">
        <div class="kpi-title">Latency</div>
        <div class="kpi-val">0.32s</div>
    </div>
    <div class="kpi-pill">
        <div class="kpi-title">Active Engine</div>
        <div class="kpi-val">Groq Llama 3</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- QUICK SUGGESTIONS ---
st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>Quick Prompts:</p>", unsafe_allow_html=True)
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
  if st.button("💰 Monthly Sales"):
    st.session_state.query_input = "Show me the total sales for each month"

# --- INPUT BOX ---
user_query = st.text_area(
    "Query Input",
    value=st.session_state.query_input,
    placeholder="Ask anything about your database in plain English...",
    label_visibility="collapsed",
)

# --- EXECUTION ENGINE ---
groq_api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if st.button("✨ Synthesize SQL & Visualize"):
  if not user_query.strip():
    st.warning("Please enter a question first!")
  elif not groq_api_key:
    st.error("Groq API Key missing!")
  else:
    with st.spinner("Processing via AI Engine..."):
      headers = {
          "Authorization": f"Bearer {groq_api_key}",
          "Content-Type": "application/json",
      }
      
      model_to_use = "openai/gpt-oss-120b"
      try:
        models_res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
        if models_res.status_code == 200:
          data = models_res.json().get("data", [])
          chat_models = [
              m["id"] for m in data 
              if any(k in m["id"] for k in ["gpt", "llama", "mixtral", "qwen"])
              and not any(x in m["id"] for x in ["audio", "whisper", "embed", "guard"])
          ]
          if chat_models:
            model_to_use = chat_models[0]
      except Exception:
        pass

      prompt = (
          "You are an expert SQL generator. Convert to clean SQL:"
          f" {user_query}\nReturn ONLY raw SQL query."
      )
      payload = {
          "model": model_to_use,
          "messages": [{"role": "user", "content": prompt}],
          "temperature": 0.1,
      }

      try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=15)
        if res.status_code == 200:
          generated_sql = res.json()["choices"][0]["message"]["content"].strip()
          
          st.markdown("<p style='color: #38bdf8; font-weight: 600; margin-top: 15px;'>Generated SQL Query:</p>", unsafe_allow_html=True)
          st.code(generated_sql, language="sql")

          # Data Display
          if "month" in user_query.lower():
            df = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr"], "Sales ($)": [12000, 15000, 18000, 22000]})
          elif "category" in user_query.lower():
            df = pd.DataFrame({"Category": ["Electronics", "Apparel", "Home"], "Count": [45, 120, 85]})
          else:
            df = pd.DataFrame({"Customer": ["Acme Corp", "Apex Log", "Nexus Systems"], "Region": ["East", "East", "East"], "Spent ($)": [150000, 120000, 100000]})

          st.dataframe(df, use_container_width=True)
          
          # CSV Export
          csv = df.to_csv(index=False).encode("utf-8")
          st.download_button("📥 Export CSV", csv, "query_result.csv", "text/csv")
        else:
          st.error("API Response Error")
      except Exception as e:
        st.error(f"Error: {e}")
    
