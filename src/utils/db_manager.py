import sqlite3
import pandas as pd
from src.utils.config import DB_PATH

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS citations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        model TEXT,
        query TEXT,
        prompt_type TEXT,
        source_url TEXT,
        source_domain TEXT,
        position INTEGER,
        context_snippet TEXT,
        authority_score REAL,
        freshness_days INTEGER
    )''')
    
    conn.commit()
    conn.close()

def save_citation(model, query, prompt_type, url, domain, position, snippet, auth_score, freshness):
    """Insert a single citation record."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''INSERT INTO citations 
                 (model, query, prompt_type, source_url, source_domain, position, context_snippet, authority_score, freshness_days)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (model, query, prompt_type, url, domain, position, snippet, auth_score, freshness))
    
    conn.commit()
    conn.close()

def load_data():
    """Load all data into a Pandas DataFrame."""
    try:
        return pd.read_sql_query("SELECT * FROM citations", sqlite3.connect(DB_PATH))
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()