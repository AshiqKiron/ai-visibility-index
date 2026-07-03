import spacy
from typing import List

# Load small English model (install via: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

KNOWN_BRANDS = [
    "Salesforce", "HubSpot", "Zoho", "Pipedrive", "Monday.com",
    "Shopify", "WooCommerce", "Magento", "BigCommerce",
    "OpenAI", "Google", "Microsoft", "Anthropic", "Meta"
]

def extract_brands(text: str) -> List[str]:
    """
    Extract brand names using both keyword matching and NER.
    """
    found_brands = set()
    
    # Method 1: Direct keyword match (case-insensitive)
    text_lower = text.lower()
    for brand in KNOWN_BRANDS:
        if brand.lower() in text_lower:
            found_brands.add(brand)
    
    # Method 2: SpaCy NER for ORG entities
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Cross-reference with known brands to reduce false positives
                for brand in KNOWN_BRANDS:
                    if brand.lower() in ent.text.lower():
                        found_brands.add(brand)
    
    return list(found_brands)