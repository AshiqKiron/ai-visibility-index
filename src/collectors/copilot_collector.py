from playwright.sync_api import sync_playwright
from src.collectors.base_collector import BaseCollector
import time

class CopilotCollector(BaseCollector):
    def __init__(self, headless=True):
        self.headless = headless
        self.url = "https://copilot.microsoft.com"

    def query(self, prompt: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.url)
            
            try:
                # Accept cookies if present
                page.click("button:has-text('Accept')", timeout=5000)
            except:
                pass

            page.wait_for_selector("#textarea", timeout=30000)
            page.fill("#textarea", prompt)
            page.press("#textarea", "Enter")
            
            # Wait for citations/sources to appear
            page.wait_for_selector(".citation", timeout=45000)
            time.sleep(2)
            
            response_text = page.text_content(".main-content")
            browser.close()
            return response_text