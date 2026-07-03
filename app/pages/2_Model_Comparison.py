import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚖️ Model Comparison Audit")

try:
    df = pd.read_csv("data/processed/metrics_summary.csv")
except FileNotFoundError:
    st.stop()

# Compare Citation Frequency by Model
st.subheader("Citation Volume by Model")
model_counts = df['model'].value_counts().reset_index()
model_counts.columns = ['Model', 'Total Citations']

fig_bar = px.bar(model_counts, x='Model', y='Total Citations', 
                 color='Model', title="How many sources does each model cite?")
st.plotly_chart(fig_bar)

# Authority Bias Comparison
st.subheader("Average Authority Score of Cited Sources")
auth_by_model = df.groupby('model')['authority_score'].mean().reset_index()

fig_auth = px.box(df, x='model', y='authority_score', 
                  title="Distribution of Authority Scores per Model")
st.plotly_chart(fig_auth)

st.info("""
**Insight:** If one model has a significantly higher average authority score, 
it may be biased toward established brands and ignore newer, niche sources.
""")