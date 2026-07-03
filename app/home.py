import streamlit as st
import pandas as pd
from pathlib import Path

# ✅ FIX: Use absolute paths relative to THIS file's location
BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"
DB_PATH = BASE_DIR / "data" / "processed" / "citations.db"

st.set_page_config(page_title="AI Visibility Index", layout="wide")
st.title(" AI Visibility & Stability Index (AVSI)")

def load_data():
    """Safely load metrics CSV with fallback handling."""
    if METRICS_PATH.exists():
        try:
            df = pd.read_csv(METRICS_PATH)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return pd.DataFrame()
    else:
        st.warning(
            "⚠️ No data found yet! The GitHub Action collector hasn't run or failed. "
            "Check the Actions tab in GitHub."
        )
        return pd.DataFrame(columns=['date', 'model', 'flicker_rate', 'authority_score', 'citation_count'])

# Load data safely
df = load_data()

# Rest of your dashboard code...
if not df.empty:
    # Your existing charts and metrics go here
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Flicker Rate", f"{df['flicker_rate'].mean():.1%}" if 'flicker_rate' in df.columns else "N/A")
    # ... rest of dashboard
else:
    st.info("Waiting for first data collection cycle...")
