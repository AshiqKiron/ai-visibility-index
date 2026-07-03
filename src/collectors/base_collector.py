from abc import ABC, abstractmethod
import time

class BaseCollector(ABC):
    def __init__(self, driver=None):
        self.driver = driver

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Send query to AI model and return raw response text."""
        pass

    def wait_for_load(self, seconds=5):
        time.sleep(seconds)