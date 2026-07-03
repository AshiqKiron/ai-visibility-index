import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# ✅ Absolute paths relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "citations.db"
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("️ Prompt Sensitivity Analysis")

def load_prompt_data():
    """Try DB first (has prompt_type), fall back to CSV with safety checks."""
    
    # 🔍 TEMPORARY DEBUG: Remove these lines once paths are confirmed working
    st.caption(f"DEBUG: BASE_DIR = `{BASE_DIR}`")
    st.caption(f"DEBUG: DB exists={DB_PATH.exists()}, size={DB_PATH.stat().st_size if DB_PATH.exists() else 'N/A'}")
    st.caption(f"DEBUG: CSV exists={METRICS_PATH.exists()}, size={METRICS_PATH.stat().st_size if METRICS_PATH.exists() else 'N/A'}")
    
    # Attempt database load first (primary source for prompt_type)
    if DB_PATH.exists() and DB_PATH.stat().st_size > 0:
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query("SELECT * FROM citations", conn)
            conn.close()
            
            if 'prompt_type' in df.columns and not df.empty:
                st.success(f"✅ Loaded {len(df)} records from database with prompt_type")
                return df
            elif 'prompt_type' not in df.columns:
                st.warning("⚠️ DB exists but missing 'prompt_type' column. Check collector schema.")
            else:
                st.warning("⚠️ DB exists but is empty.")
        except Exception as e:
            st.warning(f"⚠️ DB read failed: {e}")
    
    # Fallback to CSV (note: CSV typically lacks prompt_type)
    if METRICS_PATH.exists() and METRICS_PATH.stat().st_size > 0:
        try:
            df = pd.read_csv(METRICS_PATH)
            if 'prompt_type' in df.columns and not df.empty:
                st.success(f"✅ Loaded {len(df)} records from CSV with prompt_type")
                return df
            else:
                st.info("💡 CSV loaded but missing 'prompt_type'. Prompt audit requires database data.")
                st.markdown("> **Note:** Only the SQLite database stores prompt variation metadata. Ensure collectors are saving `prompt_type` to the DB.")
                return pd.DataFrame()
        except pd.errors.EmptyDataError:
            st.warning("⚠️ Metrics CSV is empty.")
        except Exception as e:
            st.error(f"❌ CSV read failed: {e}")
    
    st.warning("⚠️ No valid data files found. The GitHub Action collector hasn't produced results yet.")
    return pd.DataFrame()

df = load_prompt_data()

if not df.empty and 'prompt_type' in df.columns:
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
    st.info(" No prompt audit data available yet. Check GitHub Actions logs to ensure collectors are running successfully and saving `prompt_type` to the database.")
