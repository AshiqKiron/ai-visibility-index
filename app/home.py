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
    # --- FIX 1: Safe Metric Calculation ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'flicker_rate' in df.columns:
            # Convert to numeric safely, drop NaNs before averaging
            valid_rates = pd.to_numeric(df['flicker_rate'], errors='coerce').dropna()
            avg_flicker = valid_rates.mean() if not valid_rates.empty else 0
            st.metric("Avg Flicker Rate", f"{avg_flicker:.1%}")
        else:
            st.metric("Avg Flicker Rate", "N/A")
            
    with col2:
        st.metric("Models Tracked", df['model'].nunique() if 'model' in df.columns else 0)
        
    with col3:
        total_citations = df['citation_count'].sum() if 'citation_count' in df.columns else 0
        st.metric("Total Citations", f"{int(total_citations):,}")

    # --- FIX 2: Add Missing Volatility Chart ---
    st.subheader("Citation Volatility Over Time")
    
    if 'date' in df.columns and 'flicker_rate' in df.columns:
        # Ensure date is datetime for proper plotting
        df['date'] = pd.to_datetime(df['date'])
        
        fig = px.line(
            df, 
            x='date', 
            y='flicker_rate', 
            color='model',
            title="Daily Flicker Rate by Model",
            markers=True,
            template="plotly_dark"  # Matches dark theme
        )
        fig.update_layout(
            height=450,
            yaxis_title="Flicker Rate (0-1)",
            legend_title="AI Model"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chart data unavailable. Ensure 'date' and 'flicker_rate' columns exist in your dataset.")

else:
    st.info("🔍 No data available yet. The collector hasn't produced results.")
    st.markdown("""
    ### To populate this dashboard:
    1. Go to your GitHub repo → **Actions** tab  
    2. Click **Daily AI Data Collection** → **Run workflow**  
    3. Wait for the green checkmark, then **refresh this page**
    """)
