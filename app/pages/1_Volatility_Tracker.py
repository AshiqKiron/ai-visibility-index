import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📉 Volatility & Flicker Tracker")

# Load data
try:
    df = pd.read_csv("data/processed/metrics_summary.csv")
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    st.error("No metrics data found. Run the collector first.")
    st.stop()

# Filter
models = df['model'].unique()
selected_model = st.selectbox("Select Model", models)

df_filtered = df[df['model'] == selected_model]

# Plot Flicker Rate Over Time
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['flicker_rate'], 
                         mode='lines+markers', name='Flicker Rate'))

fig.update_layout(
    title=f"Flicker Rate Over Time for {selected_model}",
    xaxis_title="Date",
    yaxis_title="Flicker Rate (0-1)",
    yaxis_range=[0, 1]
)

st.plotly_chart(fig)

st.info("""
**What is Flicker Rate?**
It measures how often the #1 cited source changes from one day to the next. 
A high rate indicates instability in the AI's ranking algorithm.
""")