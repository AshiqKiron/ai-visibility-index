# 📊 AI Visibility & Stability Index (AVSI)

> A systematic framework for tracking how LLMs and AI Search engines retrieve, cite, and rank sources. This project measures the "Flicker Effect" (citation volatility) and provides actionable metrics for AI Search Optimization (AISO).

[![Daily AI Data Collection](https://github.com/AshiqKiron/ai-visibility-index/actions/workflows/collect_data.yml/badge.svg)](https://github.com/AshiqKiron/ai-visibility-index/actions/workflows/collect_data.yml)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-visibility-index.streamlit.app)

---

## 🔍 What This Project Is

The **AI Visibility & Stability Index (AVSI)** is an open-source monitoring system that treats AI search results as dynamic datasets. Unlike traditional SEO tools that track static rankings, AVSI continuously probes major AI models (ChatGPT, Gemini, Perplexity, Copilot) to measure:

-   **Citation Volatility:** How often cited sources change over time ("The Flicker Effect")
-   **Prompt Sensitivity:** How much output varies based on query phrasing
-   **Authority Bias:** Whether models favor established domains over fresh/niche sources
-   **Model Consistency:** Agreement levels between different AI platforms

It serves as both a **research instrument** for understanding generative search behavior and a **product prototype** for brand visibility monitoring.

## 💡 Why This Project Exists

AI search is fundamentally unstable. Traditional search engines have relatively predictable ranking algorithms, but LLMs exhibit:

1.  **Non-determinism:** Same query → different answers across sessions
2.  **Temporal Drift:** Rankings shift daily without clear signals
3.  **Prompt Fragility:** Minor wording changes dramatically alter citations
4.  **Black Box Attribution:** No transparency into why specific sources are chosen

Brands and publishers currently have **no reliable way to measure or optimize** for AI visibility. AVSI fills this gap by providing empirical, reproducible metrics instead of anecdotal observations.

## 🎯 Goals

| Goal | Description |
| :--- | :--- |
| **Quantify Instability** | Create standardized metrics (Flicker Rate, CSI, PSI) to measure AI search volatility |
| **Identify Drivers** | Determine which factors (authority, freshness, prompt type) most influence citations |
| **Enable Monitoring** | Provide brands with a dashboard to track their AI visibility health over time |
| **Fuel Research** | Generate original data for thought leadership reports on the state of AI search |
| **Open Source Foundation** | Build a reusable framework others can extend for their own AI search research |

## 🏗️ Architecture

The system follows a linear CI/CD-inspired pipeline where data collection, processing, and visualization are decoupled:

```text
┌─────────────────────┐
│   GitHub Actions    │
│  (Daily Scheduler)  │
└──────────┬──────────┘
           │ Triggers every 24h
           ▼
┌─────────────────────
│  Playwright Bots    │
│ (Headless Scrapers) │
└──────────┬──────────┘
           │ Raw HTML + Citations
           ▼
┌─────────────────────┐
│  Processing Layer   │
│ (SQLite + Pandas)   │
└──────────┬──────────┘
           │ Enriched Metrics CSV
           ▼
┌─────────────────────┐
│   Streamlit Cloud   │
│  (Live Dashboard)   │
──────────────────────┘
```

### Key Components

-   **Collector Engine:** Python + Playwright scripts that simulate user queries across 5 AI platforms
-   **Data Store:** SQLite database for raw citations + CSV for aggregated daily metrics
-   **Analysis Module:** Custom Python scripts calculating Flicker Rate, Authority Scores, and Prompt Sensitivity
-   **Visualization:** Interactive Streamlit app with Plotly charts for real-time exploration

## ️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Automation** | GitHub Actions | Scheduled data collection & CI/CD |
| **Scraping** | Playwright + Chromium | Headless browser automation for AI interfaces |
| **Data Storage** | SQLite + Pandas | Lightweight local database + analysis |
| **NLP/Enrichment** | spaCy + VADER | Brand extraction + sentiment analysis |
| **Visualization** | Streamlit + Plotly | Interactive dashboard hosting |
| **ML Analysis** | scikit-learn | Regression models for citation drivers |
| **Hosting** | Streamlit Cloud + GitHub Pages | Free live demo + research landing page |

## ⚡ Latency & Performance

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Data Freshness** | ~24 hours | Updated once daily via cron schedule |
| **Dashboard Load** | < 3 seconds | Pre-aggregated CSV loads instantly |
| **Collection Runtime** | 8-12 minutes | Depends on AI model response times |
| **Chart Rendering** | < 1 second | Plotly client-side rendering |

> **Note:** Real-time scraping is intentionally avoided to respect AI platform rate limits and reduce infrastructure costs. Near-real-time updates can be enabled via manual workflow triggers.

##  Cost Breakdown

This entire stack operates at **$0/month** using free tiers:

| Component | Service | Cost | Limit |
| :--- | :--- | :--- | :--- |
| Compute | GitHub Actions | Free | 2,000 min/month |
| Hosting | Streamlit Cloud | Free | Community tier |
| Static Site | GitHub Pages | Free | Unlimited |
| Browser Automation | Playwright | Free | Open source |
| Database | SQLite | Free | Local file |
| NLP Models | spaCy/VADER | Free | Open source |

> **Scaling Note:** If you exceed GitHub Actions minutes or need faster updates, estimated cost would be ~$5-10/month for GitHub Pro + a basic VPS.

## ️ Trade-offs

| Decision | Benefit | Cost |
| :--- | :--- | :--- |
| **Headless browsers vs APIs** | Captures exact UI-rendered citations | Slower, more fragile to UI changes |
| **SQLite vs PostgreSQL** | Zero setup, portable, no server needed | No concurrent writes, limited scale |
| **Daily batch vs real-time** | Respects rate limits, $0 cost | 24h latency on insights |
| **Mock authority scores** | Works offline, no API keys needed | Not ground-truth DA/PA values |
| **Streamlit vs custom React** | Fast prototyping, Python-native | Less customizable UI/UX |

## 🚧 Limitations

1.  **UI Dependency:** Collectors rely on CSS selectors that break when AI platforms update their frontend. Requires maintenance.
2.  **Authentication Wall:** Free-tier AI models require logged-in sessions; automated login is brittle and may violate ToS.
3.  **Rate Limiting:** Aggressive scraping risks IP bans. Current implementation includes conservative delays.
4.  **Geographic Bias:** Results reflect the runner's location (US-based GitHub Actions). Regional variations aren't captured.
5.  **No Ground Truth:** There is no "correct" answer for AI citations; we measure consistency, not accuracy.
6.  **Single-Threaded:** GitHub Actions runners are single-core; parallelizing queries requires self-hosted runners.

## 🚀 Quick Start

### Prerequisites
-   Python 3.10+
-   Git

### Installation

```bash
git clone https://github.com/AshiqKiron/ai-visibility-index.git
cd ai-visibility-index
pip install -r requirements.txt
playwright install chromium
```

### Run locally

1. Collect data (mock mode by default)
python src/collectors/run_all_collectors.py

2. Process metrics
python analysis/volatility_metrics.py

3. Launch dashboard
streamlit run app/home.py

### Deploy to Streamlit Cloud
- Push code to GitHub main branch
- Go to share.streamlit.io → New App
- Select repo, branch main, main file app/home.py
- Click Deploy
