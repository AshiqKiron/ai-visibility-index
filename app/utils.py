import pandas as pd
import sqlite3
from pathlib import Path
from functools import lru_cache

DB_PATH = Path("data/processed/citations.db")

@lru_cache(maxsize=1)
def load_full_dataset() -> pd.DataFrame:
    """Load and cache the full citations dataset."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM citations", conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return pd.DataFrame()

def get_unique_models() -> list:
    df = load_full_dataset()
    return sorted(df['model'].unique().tolist()) if not df.empty else []

def get_query_categories() -> list:
    df = load_full_dataset()
    return sorted(df['category'].dropna().unique().tolist()) if 'category' in df.columns else []

def filter_data(df: pd.DataFrame, model: str = None, category: str = None) -> pd.DataFrame:
    """Apply sidebar filters to dataframe."""
    filtered = df.copy()
    if model and model != "All":
        filtered = filtered[filtered['model'] == model]
    if category and category != "All":
        filtered = filtered[filtered['category'] == category]
    return filtered