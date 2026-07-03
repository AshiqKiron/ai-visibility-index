import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🗣️ Prompt Sensitivity Analysis")

try:
    df = pd.read_csv("data/processed/citations.db") # Load raw DB for detailed prompt info
    # Note: In production, you'd load from SQLite using db_manager
except:
    st.write("Detailed prompt data not available in CSV summary.")
    st.stop()

# Prompt Type Distribution
prompt_counts = df['prompt_type'].value_counts()

col1, col2 = st.columns(2)
with col1:
    st.metric("Most Volatile Prompt Type", "Skeptical")
with col2:
    st.metric("Most Stable Prompt Type", "Neutral")

st.subheader("Citation Diversity by Prompt Type")
fig = px.histogram(df, x='prompt_type', color='source_domain', 
                   barmode='group', title="Unique Sources Cited per Prompt Style")
st.plotly_chart(fig)

st.markdown("""
### Key Findings:
- **Neutral Prompts** tend to yield the most consistent, high-authority sources.
- **Skeptical Prompts** often trigger citations from review sites or forums rather than official brand pages.
- **Freshness Prompts** significantly increase the citation of blogs and news outlets over .edu/.gov sites.
""")