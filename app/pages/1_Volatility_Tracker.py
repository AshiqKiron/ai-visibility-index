import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ✅ Absolute path relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_DIR / "data" / "processed" / "metrics_summary.csv"

st.title("📉 Volatility & Flicker Tracker")

def load_volatility_data():
    if METRICS_PATH.exists():
        try:
            df = pd.read_csv(METRICS_PATH)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            st.error(f"Error loading volatility data: {e}")
            return pd.DataFrame()
    else:
        st.warning("️ No metrics data found. Run the GitHub Action collector first.")
        return pd.DataFrame()

df = load_volatility_data()

if not df.empty and 'model' in df.columns:
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
    st.info("No volatility data available yet. Waiting for first collection cycle...")
