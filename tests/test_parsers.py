import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import unittest
from src.parsers.url_extractor import extract_urls
from src.parsers.brand_extractor import extract_brands
from src.parsers.sentiment_analyzer import get_sentiment_label

class TestURLExtractor(unittest.TestCase):
    def test_extract_multiple_urls(self):
        text = "Visit https://example.com and http://test.org/page for info."
        urls = extract_urls(text)
        self.assertEqual(len(urls), 2)

    def test_clean_trailing_punctuation(self):
        text = "See https://example.com)."
        urls = extract_urls(text)
        self.assertEqual(urls[0], "https://example.com")

class TestBrandExtractor(unittest.TestCase):
    def test_known_brand_detection(self):
        text = "Many companies use Salesforce and HubSpot for CRM."
        brands = extract_brands(text)
        self.assertIn("Salesforce", brands)

class TestSentimentAnalyzer(unittest.TestCase):
    def test_positive_sentiment(self):
        label = get_sentiment_label("This tool is excellent!")
        self.assertEqual(label, "Positive")

if __name__ == '__main__':
    unittest.main()
