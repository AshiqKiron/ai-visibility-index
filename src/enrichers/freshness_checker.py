import requests
from datetime import datetime

def get_freshness_days(url: str) -> int:
    """
    Calculate days since the last modification of a URL.
    """
    try:
        headers = requests.head(url, timeout=5, allow_redirects=True).headers
        last_modified = headers.get('Last-Modified')
        
        if last_modified:
            # Format: Tue, 15 Nov 1994 08:12:31 GMT
            fmt = "%a, %d %b %Y %H:%M:%S %Z"
            mod_date = datetime.strptime(last_modified, fmt)
            delta = datetime.now() - mod_date
            return delta.days
        else:
            return 999 # Unknown freshness
    except Exception:
        return 999 # Error fetching