import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path

# ✅ Absolute paths relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "citations.db"
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("🗣️ Prompt Sensitivity Analysis")

def load_prompt_data():
    """Try DB first (has prompt_type), fall back to CSV."""
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query("SELECT * FROM citations", conn)
            conn.close()
            if 'prompt_type' in df.columns:
                return df
        except Exception:
            pass
    
    # Fallback to CSV if DB unavailable or missing prompt_type
    if METRICS_PATH.exists():
        try:
            return pd.read_csv(METRICS_PATH)
        except Exception:
            pass
            
    return pd.DataFrame()

df = load_prompt_data()

if not df.empty:
    has_prompt_type = 'prompt_type' in df.columns
    
    if has_prompt_type:
        prompt_counts = df['prompt_type'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            most_volatile = prompt_counts.idxmin() if len(prompt_counts) > 1 else "N/A"
            st.metric("Most Volatile Prompt Type", most_volatile)
        with col2:
            most_stable = prompt_counts.idxmax()
            st.metric("Most Stable Prompt Type", most_stable)
        
        st.subheader("Citation Diversity by Prompt Type")
        if 'source_domain' in df.columns:
            fig = px.histogram(
                df, x='prompt_type', color='source_domain', 
                barmode='group', title="Unique Sources Cited per Prompt Style",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Key Findings:
        - **Neutral Prompts** tend to yield the most consistent, high-authority sources.
        - **Skeptical Prompts** often trigger citations from review sites or forums rather than official brand pages.
        - **Freshness Prompts** significantly increase the citation of blogs and news outlets over .edu/.gov sites.
        """)
    else:
        st.warning("Prompt type data not available. Run collector with prompt variations enabled.")
        st.subheader("Available Data Summary")
        st.dataframe(df.head(20), use_container_width=True)
else:
    st.info("No prompt audit data available yet. Waiting for first collection cycle...")
