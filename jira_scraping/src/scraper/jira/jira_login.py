"""Jira login functionality."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import settings
import time


class JiraLogin:
    """Handles Jira authentication flow."""
    
    def __init__(self, driver):
        self.driver = driver
        self.login_done = False
    
    def login(self, max_attempts=2):
        """Perform Jira login with retry logic."""
        attempt = 1
        while attempt <= max_attempts:
            print(f"[INFO] Login attempt {attempt} of {max_attempts}")
            try:
                self._perform_login_attempt()
                self.login_done = True
                return

            except Exception as e:
                self._handle_login_error(e, attempt, max_attempts)
            attempt += 1
    
    def _perform_login_attempt(self):
        """Perform a single login attempt."""
        wait = WebDriverWait(self.driver, 40)
        LOGIN_URL = settings.LOGIN_URL  
        self.driver.get(LOGIN_URL)

        # Step 1: Enter email
        print("Step 1: waiting for email field...")
        email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-testid="username"]')))
        email_input.clear()
        email_input.send_keys(settings.JIRA_USERNAME)

        continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        continue_btn.click()

        # Step 2: Enter password
        print("Step 2: waiting for password field...")
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.clear()
        password_input.send_keys(settings.JIRA_PASSWORD)

        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        login_btn.click()

        # Step 3: Handle optional verification
        self._handle_optional_verification()

        # Step 4: Wait for successful login
        print("Step 4: waiting for Jira dashboard...")
        wait.until(lambda d: "atlassian.net" in d.current_url)
        print("After login, current URL is:", self.driver.current_url)
    
    def _handle_optional_verification(self):
        """Handle optional 2FA or verification step."""
        try:
            print("Step 3: checking for extra verification...")
            verify_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Verify') or contains(., 'Continue')]"))
            )
            verify_btn.click()
            print("Extra verification step clicked.")
        except TimeoutException:
            print("No extra verification step detected.")
    
    def _handle_login_error(self, error, attempt, max_attempts):
        """Handle login errors with retry logic."""
        print(f"[ERROR] Login attempt {attempt} failed: {type(error).__name__} - {error}")
        # screenshot_path = f"login_failed_attempt_{attempt}.png"
        # self.driver.save_screenshot(screenshot_path)
        # print(f"[DEBUG] Screenshot saved: {screenshot_path}")

        if attempt < max_attempts:
            print("[INFO] Retrying in 5 seconds...")
            time.sleep(5)
        else:
            print("[FATAL] All login attempts failed.")
            raise
