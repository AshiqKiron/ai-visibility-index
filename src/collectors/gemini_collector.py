from playwright.sync_api import sync_playwright
from src.collectors.base_collector import BaseCollector
import time

class GeminiCollector(BaseCollector):
    def __init__(self, headless=True):
        self.headless = headless
        self.url = "https://gemini.google.com"

    def query(self, prompt: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(self.url)
            
            # Wait for the input area to be ready
            try:
                page.wait_for_selector("div[role='textbox']", timeout=30000)
                page.fill("div[role='textbox']", prompt)
                
                # Handle the "Enter" or "Send" button click
                # Selector might vary based on UI updates
                page.keyboard.press("Enter")
                
                # Wait for the response to start rendering
                page.wait_for_selector(".response-container", timeout=60000)
                time.sleep(3) # Allow full render
                
                response_text = page.text_content("main")
                browser.close()
                return response_text
            except Exception as e:
                print(f"Gemini Error: {e}")
                browser.close()
                return ""