import sys
from pathlib import Path

# ✅ Universal path fix for Streamlit Cloud + local dev
if '/mount/src/' in str(Path.cwd()):
    PROJECT_ROOT = Path('/mount/src/ai-visibility-index')
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

BASE_DIR = PROJECT_ROOT
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("⚖️ Model Comparison Audit")

def load_comparison_data():
    """Safely load comparison data with file validation."""
    if not METRICS_PATH.exists():
        st.warning("⚠️ No metrics file found. The GitHub Action collector hasn't run yet.")
        return pd.DataFrame()
    
    if METRICS_PATH.stat().st_size == 0:
        st.warning("⚠️ Data file exists but is empty. Collector produced no results.")
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
        st.warning("⚠️ Empty data file. Run the GitHub Action collector first.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading comparison data: {str(e)}")
        return pd.DataFrame()

df = load_comparison_data()

if not df.empty:
    st.subheader("Citation Volume by Model")
    model_counts = df['model'].value_counts().reset_index()
    model_counts.columns = ['Model', 'Total Citations']
    
    fig_bar = px.bar(
        model_counts, x='Model', y='Total Citations', 
        color='Model', title="How many sources does each model cite?",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
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
    st.info("🔍 No comparison data available yet. Check GitHub Actions logs to ensure collectors are running successfully.")
