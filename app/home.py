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

BASE_DIR = PROJECT_ROOT
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.set_page_config(page_title="AI Visibility Index", layout="wide")
st.title("📊 AI Visibility & Stability Index (AVSI)")
st.markdown("Tracking citation behavior, volatility, and flicker effects across major AI models.")

def load_data():
    """Safely load metrics CSV with comprehensive error handling."""
    if not METRICS_PATH.exists():
        return pd.DataFrame()
    
    if METRICS_PATH.stat().st_size == 0:
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(METRICS_PATH)
        required_cols = ['date', 'model']
        if not all(c in df.columns for c in required_cols):
            st.error(f"Malformed CSV. Missing columns: {[c for c in required_cols if c not in df.columns]}")
            return pd.DataFrame()
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_flicker = df['flicker_rate'].mean() if 'flicker_rate' in df.columns else 0
        st.metric("Avg Flicker Rate", f"{avg_flicker:.1%}")
    with col2:
        st.metric("Models Tracked", df['model'].nunique() if 'model' in df.columns else 0)
    with col3:
        total_citations = df['citation_count'].sum() if 'citation_count' in df.columns else 0
        st.metric("Total Citations", f"{total_citations:,}")

    st.subheader("Citation Volatility Over Time")
    # Add your existing chart code here when data is populated
else:
    st.info("🔍 No data available yet. The collector hasn't produced results.")
    st.markdown("""
    ### To populate this dashboard:
    1. Go to your GitHub repo → **Actions** tab  
    2. Click **Daily AI Data Collection** → **Run workflow**  
    3. Wait for the green checkmark, then **refresh this page**
    
    > 💡 If the Action keeps failing, check the logs under the 
    > "Execute AI Scrapers" step for authentication or timeout errors.
    """)
