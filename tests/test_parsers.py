import unittest
from src.parsers.url_extractor import extract_urls, extract_brands
from src.parsers.sentiment_analyzer import get_sentiment_label

class TestURLExtractor(unittest.TestCase):
    def test_extract_multiple_urls(self):
        text = "Visit https://example.com and http://test.org/page for info."
        urls = extract_urls(text)
        self.assertEqual(len(urls), 2)
        self.assertIn("https://example.com", urls)

    def test_clean_trailing_punctuation(self):
        text = "See https://example.com)."
        urls = extract_urls(text)
        self.assertEqual(urls[0], "https://example.com")

    def test_no_urls(self):
        self.assertEqual(extract_urls("No links here"), [])

class TestBrandExtractor(unittest.TestCase):
    def test_known_brand_detection(self):
        text = "Many companies use Salesforce and HubSpot for CRM."
        brands = extract_brands(text)
        self.assertIn("Salesforce", brands)
        self.assertIn("HubSpot", brands)

    def test_case_insensitive(self):
        text = "shopify is popular"
        brands = extract_brands(text)
        self.assertIn("Shopify", brands)

class TestSentimentAnalyzer(unittest.TestCase):
    def test_positive_sentiment(self):
        label = get_sentiment_label("This tool is excellent and highly recommended!")
        self.assertEqual(label, "Positive")

    def test_negative_sentiment(self):
        label = get_sentiment_label("Terrible experience, completely broken and useless.")
        self.assertEqual(label, "Negative")

    def test_neutral_sentiment(self):
        label = get_sentiment_label("The software was released in 2020.")
        self.assertEqual(label, "Neutral")

if __name__ == '__main__':
    unittest.main()