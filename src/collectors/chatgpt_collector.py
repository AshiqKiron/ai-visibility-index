from playwright.sync_api import sync_playwright
from src.collectors.base_collector import BaseCollector
import time

class ChatGPTCollector(BaseCollector):
    def __init__(self, headless=True):
        self.headless = headless
        self.url = "https://chat.openai.com"

    def query(self, prompt: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            # Navigate and wait for user to be logged in (manual step for free tier)
            page.goto(self.url)
            page.wait_for_selector("textarea", timeout=30000) 
            
            # Type prompt
            page.fill("textarea", prompt)
            page.press("textarea", "Enter")
            
            # Wait for response
            page.wait_for_selector(".markdown", timeout=60000)
            time.sleep(2) # Extra buffer for rendering
            
            # Extract text
            response_text = page.text_content(".markdown")
            browser.close()
            return response_text