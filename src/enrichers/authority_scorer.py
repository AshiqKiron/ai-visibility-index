import hashlib
import json
from pathlib import Path
from functools import lru_cache

CACHE_FILE = Path("data/cache/authority_cache.json")

def _load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def _save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache))

@lru_cache(maxsize=500)
def get_authority_score(domain: str) -> float:
    """
    Get Domain Authority score with local caching.
    Replace mock logic with Moz/Ahrefs API calls in production.
    """
    cache = _load_cache()
    
    if domain in cache:
        return cache[domain]
    
    # --- MOCK SCORING LOGIC (Replace with API) ---
    hash_val = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    score = (hash_val % 80) + 10  # Base score 10-90
    
    # Manual overrides for known high-authority domains
    overrides = {
        "wikipedia.org": 98, "nytimes.com": 94, "bbc.com": 93,
        "nature.com": 96, "science.org": 95, "harvard.edu": 97,
        "stanford.edu": 96, "mit.edu": 97, "github.com": 91
    }
    
    for key, val in overrides.items():
        if key in domain:
            score = val
            break
    
    if ".gov" in domain:
        score = max(score, 92)
    if ".edu" in domain:
        score = max(score, 88)
    # -------------------------------------------
    
    cache[domain] = score
    _save_cache(cache)
    return score

def get_freshness_days(url: str) -> int:
    """Check Last-Modified header for content freshness."""
    import requests
    from datetime import datetime
    
    try:
        headers = requests.head(url, timeout=5, allow_redirects=True).headers
        last_mod = headers.get('Last-Modified')
        if last_mod:
            fmt = "%a, %d %b %Y %H:%M:%S %Z"
            mod_date = datetime.strptime(last_mod, fmt)
            return (datetime.now() - mod_date).days
    except Exception:
        pass
    return 999  # Unknown