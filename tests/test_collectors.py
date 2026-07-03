import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import unittest
from unittest.mock import patch, MagicMock
from src.collectors.base_collector import BaseCollector
from src.collectors.chatgpt_collector import ChatGPTCollector
from src.collectors.perplexity_collector import PerplexityCollector

class TestBaseCollector(unittest.TestCase):
    def test_abstract_method(self):
        with self.assertRaises(TypeError):
            BaseCollector()

class TestChatGPTCollector(unittest.TestCase):
    @patch('src.collectors.chatgpt_collector.sync_playwright')
    def test_query_returns_string(self, mock_playwright):
        mock_page = MagicMock()
        mock_page.text_content.return_value = "Test response"
        mock_browser = MagicMock()
        mock_browser.new_page.return_value = mock_page
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        
        collector = ChatGPTCollector(headless=True)
        result = collector.query("test prompt")
        
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Test response")

if __name__ == '__main__':
    unittest.main()
