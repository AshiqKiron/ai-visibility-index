import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ✅ Absolute path relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("📉 Volatility & Flicker Tracker")

def load_volatility_data():
    """Safely load volatility data with comprehensive error handling."""
    if not METRICS_PATH.exists():
        st.warning("⚠️ No metrics file found. The GitHub Action collector hasn't run yet.")
        return pd.DataFrame()
    
    # Check for empty file before parsing
    if METRICS_PATH.stat().st_size == 0:
        st.warning("⚠️ Data file exists but is empty. Collector produced no results.")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(METRICS_PATH)
        
        # Validate required columns exist
        required_cols = ['date', 'model', 'flicker_rate']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            st.error(f"Data file malformed. Missing columns: {missing}")
            return pd.DataFrame()
            
        if df.empty:
            st.warning("⚠️ Data file has headers but no rows. Waiting for collection...")
            return pd.DataFrame()
            
        df['date'] = pd.to_datetime(df['date'])
        return df
        
    except pd.errors.EmptyDataError:
        st.warning("⚠️ Empty data file. Run the GitHub Action collector first.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading volatility data: {str(e)}")
        return pd.DataFrame()

df = load_volatility_data()

if not df.empty:
    models = sorted(df['model'].unique())
    selected_model = st.selectbox("Select Model", models)
    
    df_filtered = df[df['model'] == selected_model].sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['date'], 
        y=df_filtered['flicker_rate'], 
        mode='lines+markers', 
        name='Flicker Rate',
        line=dict(color='#FF4B4B', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=f"Flicker Rate Over Time for {selected_model}",
        xaxis_title="Date",
        yaxis_title="Flicker Rate (0-1)",
        yaxis_range=[0, max(1, df_filtered['flicker_rate'].max() * 1.2)],
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **What is Flicker Rate?**
    It measures how often the #1 cited source changes from one day to the next. 
    A high rate (>0.5) indicates instability in the AI's ranking algorithm.
    """)
else:
    st.info(" No volatility data available yet. Check GitHub Actions logs to ensure collectors are running successfully.")
