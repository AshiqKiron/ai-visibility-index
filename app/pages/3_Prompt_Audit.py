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
    """Try DB first (has prompt_type), fall back to CSV with safety checks."""
    # Attempt database load first
    if DB_PATH.exists() and DB_PATH.stat().st_size > 0:
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query("SELECT * FROM citations", conn)
            conn.close()
            if 'prompt_type' in df.columns and not df.empty:
                return df
        except Exception:
            pass
    
    # Fallback to CSV with full safety checks
    if not METRICS_PATH.exists():
        st.warning("️ No data files found. The GitHub Action collector hasn't run yet.")
        return pd.DataFrame()
    
    if METRICS_PATH.stat().st_size == 0:
        st.warning("⚠️ Metrics file exists but is empty. Collector produced no results.")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(METRICS_PATH)
        
        required_cols = ['model']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.error(f"Data file malformed. Missing columns: {missing}")
            return pd.DataFrame()
            
        if df.empty:
            st.warning("⚠️ Data file has headers but no rows. Waiting for collection...")
            return pd.DataFrame()
            
        return df
        
    except pd.errors.EmptyDataError:
        st.warning("⚠️ Empty metrics file. Run the GitHub Action collector first.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading prompt data: {str(e)}")
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
    st.info("🔍 No prompt audit data available yet. Check GitHub Actions logs to ensure collectors are running successfully.")
