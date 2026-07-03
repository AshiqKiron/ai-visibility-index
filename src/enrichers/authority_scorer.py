import hashlib

def get_authority_score(domain: str) -> float:
    """
    Mock function to simulate Domain Authority (0-100).
    Replace this with actual API calls to Moz/Majestic/Ubersuggest.
    """
    # Deterministic mock based on domain name for consistency
    hash_val = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    score = (hash_val % 100) + 1
    
    # Boost known authoritative domains manually for demo purposes
    if "wikipedia.org" in domain: return 98
    if ".gov" in domain: return 95
    if ".edu" in domain: return 92
    if "nytimes.com" in domain: return 90
    
    return score

def get_freshness_days(url: str) -> int:
    """
    Mock function to simulate days since last update.
    Replace with requests.head() to check Last-Modified header.
    """
    # Random mock between 1 and 365 days
    import random
    return random.randint(1, 365)