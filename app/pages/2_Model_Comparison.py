import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ✅ Absolute path relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("⚖️ Model Comparison Audit")

def load_comparison_data():
    if METRICS_PATH.exists():
        try:
            return pd.read_csv(METRICS_PATH)
        except Exception as e:
            st.error(f"Error loading comparison data: {e}")
            return pd.DataFrame()
    else:
        st.warning("⚠️ No metrics data found. Run the GitHub Action collector first.")
        return pd.DataFrame()

df = load_comparison_data()

if not df.empty and 'model' in df.columns:
    # Citation Volume by Model
    st.subheader("Citation Volume by Model")
    model_counts = df['model'].value_counts().reset_index()
    model_counts.columns = ['Model', 'Total Citations']
    
    fig_bar = px.bar(
        model_counts, x='Model', y='Total Citations', 
        color='Model', title="How many sources does each model cite?",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Authority Bias Comparison
    st.subheader("Average Authority Score of Cited Sources")
    if 'authority_score' in df.columns:
        fig_auth = px.box(
            df, x='model', y='authority_score', 
            title="Distribution of Authority Scores per Model",
            color='model', template="plotly_white"
        )
        st.plotly_chart(fig_auth, use_container_width=True)
        
        st.info("""
        **Insight:** If one model has a significantly higher average authority score, 
        it may be biased toward established brands and ignore newer, niche sources.
        """)
    else:
        st.warning("Authority score data not available in current dataset.")
else:
    st.info("No comparison data available yet. Waiting for first collection cycle...")
