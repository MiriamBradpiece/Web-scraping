from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from config import settings


class BaseScraper(ABC):
    """Abstract base class for Selenium-based scrapers."""

    def __init__(self, base_url: str, headless: bool = settings.HEADLESS):
        self.base_url = base_url
        self.driver = self._init_driver(headless)
        self.login_done = False

    def _init_driver(self, headless: bool):
        """Initialize Chrome WebDriver."""
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def open_page(self, url: str):
        """Open a given page."""
        self.driver.get(url)
        time.sleep(2)  # Small delay for page to load

    @abstractmethod
    def login(self):
        """Abstract method for logging into the site."""
        pass

    @abstractmethod
    def scrape(self):
        """Abstract method for scraping."""
        pass

    def close(self):
        """Close the browser."""
        self.driver.quit()



