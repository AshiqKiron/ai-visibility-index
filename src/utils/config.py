import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data Paths
DATA_DIR = BASE_DIR / "data"
QUERIES_FILE = DATA_DIR / "queries.csv"
DB_PATH = DATA_DIR / "processed" / "citations.db"

# Models to Test
MODELS = ["chatgpt", "gemini", "perplexity", "copilot"]

# Prompt Templates
PROMPT_TEMPLATES = {
    "neutral": "What are the best {topic}?",
    "authority": "According to industry experts, what are the top {topic}?",
    "freshness": "What are the newest {topic} in 2026?",
    "skeptical": "What are the common criticisms of {topic}?"
}

# Browser Settings (for Selenium/Playwright)
HEADLESS = True
WAIT_TIME = 10  # seconds