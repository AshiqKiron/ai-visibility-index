import unittest
from src.parsers.url_extractor import extract_urls

class TestParsers(unittest.TestCase):
    
    def test_extract_urls_basic(self):
        text = "Check out https://example.com and www.google.com for more."
        urls = extract_urls(text)
        self.assertIn("https://example.com", urls)
        self.assertIn("www.google.com", urls)

    def test_extract_urls_empty(self):
        text = "No links here."
        urls = extract_urls(text)
        self.assertEqual(len(urls), 0)

if __name__ == '__main__':
    unittest.main()