import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
DB_PATH = Path("../data/processed/citations.db")
st.set_page_config(page_title="AI Visibility Index", layout="wide")

st.title("📊 AI Visibility & Stability Index (AVSI)")
st.markdown("Tracking citation behavior, volatility, and flicker effects across major AI models.")

# Sidebar filters
model = st.sidebar.selectbox("Select Model", ["All", "ChatGPT", "Gemini", "Perplexity", "Copilot"])
query_category = st.sidebar.multiselect("Category", ["Factual", "Commercial", "Trending"])

# Load Data (Mock function for demo)
def load_data():
    # In production, connect to SQLite
    return pd.read_csv("../data/processed/metrics_summary.csv")

df = load_data()

# Key Metrics Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Flicker Rate", "24%", "-2%")
with col2:
    st.metric("Top Stable Source", "Wikipedia", "CSI: 98%")
with col3:
    st.metric("Models Tested", "5")

# Volatility Chart
st.subheader("Citation Volatility Over Time")
fig = px.line(df, x='date', y='flicker_rate', color='model', title="Daily Flicker Rate by Model")
st.plotly_chart(fig)

# Source Authority vs Citation Frequency
st.subheader("Authority Score vs. Citation Frequency")
fig_scatter = px.scatter(df, x='authority_score', y='citation_count', 
                         color='model', size='freshness_score',
                         title="Do High-Authority Sites Get Cited More?")
st.plotly_chart(fig_scatter)