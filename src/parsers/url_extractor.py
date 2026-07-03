import re

def extract_urls(text: str) -> list:
    """Extract URLs from AI response text."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = re.findall(url_pattern, text)
    return [url.rstrip(').') for url in urls] # Clean trailing punctuation

def extract_brands(text: str, brand_list: list) -> list:
    """Simple keyword matching for known brands."""
    found_brands = [brand for brand in brand_list if brand.lower() in text.lower()]
    return list(set(found_brands))