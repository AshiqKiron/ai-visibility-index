from playwright.sync_api import sync_playwright
from src.collectors.base_collector import BaseCollector
import time

class PerplexityCollector(BaseCollector):
    def __init__(self, headless=True):
        self.headless = headless
        self.url = "https://www.perplexity.ai"

    def query(self, prompt: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.url)
            
            # Handle cookie banner if present
            try:
                page.click("button:has-text('Accept')", timeout=5000)
            except:
                pass

            page.fill("textarea[placeholder='Ask anything...']", prompt)
            page.press("textarea[placeholder='Ask anything...']", "Enter")
            
            # Wait for sources to appear
            page.wait_for_selector(".source-citation", timeout=45000)
            time.sleep(2)
            
            # Get full response including sources
            response_text = page.text_content("body")
            browser.close()
            return response_text