"""Main Jira scraper orchestrator."""

from scraper.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import settings

from .jira_login import JiraLogin
from .jira_extractors import JiraExtractors
from .jira_utils import JiraUtils


class JiraScraper(BaseScraper):
    """Main Jira scraper that orchestrates the scraping process."""
    
    def __init__(self, headless: bool = settings.HEADLESS):
        super().__init__(settings.JIRA_URL, headless)  # Get base_url from settings
        self.login_handler = JiraLogin(self.driver)

    def login(self, max_attempts=2):
        """Perform Jira login."""
        self.login_handler.login(max_attempts)

    def scrape(self):
        """Main scraping method that orchestrates the entire process."""
        if not self.login_handler.login_done:
            self.login()

        try:
            self._navigate_to_issues_page()
            rows = JiraUtils.find_issue_rows(self.driver)
            
            if not rows:
                return JiraUtils.fallback_extraction(self.driver)
            
            return self._extract_issues_from_rows(rows)
            
        except Exception as e:
            return JiraUtils.handle_scraping_error(self.driver, e)

    def _navigate_to_issues_page(self):
        """Navigate to the Jira issues page and wait for it to load."""
        self.open_page(f"{self.base_url}/issues/?jql=ORDER%20BY%20created%20DESC")
        print(f"Opened page: {self.driver.current_url}")
        
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/browse/']")))

    def _extract_issues_from_rows(self, rows):
        """Extract issue information from found rows."""
        issues = []
        total_rows = len(rows)
        print(f"Processing all {total_rows} rows")
        
        # First pass: extract all basic data (without descriptions)
        print("Phase 1: Extracting basic issue data...")
        for i, row in enumerate(rows):
            try:
                print(f"Processing row {i+1}/{total_rows}")
                issue_data = self._extract_issue_data_from_row_without_description(row, i+1)
                if issue_data:
                    issues.append(issue_data)
                    print(f"  Successfully extracted: {issue_data['key']}")
                else:
                    print(f"  No data extracted from row {i+1}")
                    
            except Exception as e:
                print(f"ERROR processing row {i+1}: {type(e).__name__} - {e}")
                continue

        print(f"Phase 1 complete: Found {len(issues)} issues")
        
        # Second pass: fetch descriptions
        print("Phase 2: Fetching descriptions...")
        for i, issue in enumerate(issues):
            try:
                print(f"Fetching description for {i+1}/{len(issues)}: {issue['key']}")
                description = self._fetch_issue_description(issue['url'])
                issue['description'] = description
                    
            except Exception as e:
                print(f"ERROR fetching description for {issue['key']}: {type(e).__name__} - {e}")
                issue['description'] = "Error fetching description"
                continue

        print(f"Found {len(issues)} issues total")
        return issues

    def _extract_issue_data_from_row(self, row, row_number):
        """Extract all issue data from a single row."""
        # Extract issue key and URL
        key_data = JiraExtractors.extract_issue_key(row, row_number)
        if not key_data:
            return None
            
        issue_key, issue_url = key_data
        
        # Extract other fields
        summary = JiraExtractors.extract_summary(row)
        reporter = JiraExtractors.extract_reporter(row, row_number)
        priority = JiraExtractors.extract_priority(row)
        status = JiraExtractors.extract_status(row)
        created = JiraExtractors.extract_created(row)
        updated = JiraExtractors.extract_updated(row)
        
        # Fetch detailed description from the issue page
        description = self._fetch_issue_description(issue_url)
        
        return {
            "key": issue_key,
            "url": issue_url,
            "summary": summary,
            "reporter": reporter,
            "priority": priority,
            "status": status,
            "created": created,
            "updated": updated,
            "description": description
        }

    def _extract_issue_data_from_row_without_description(self, row, row_number):
        """Extract all issue data from a single row except description."""
        # Extract issue key and URL
        key_data = JiraExtractors.extract_issue_key(row, row_number)
        if not key_data:
            return None
            
        issue_key, issue_url = key_data
        
        # Extract other fields
        summary = JiraExtractors.extract_summary(row)
        reporter = JiraExtractors.extract_reporter(row, row_number)
        priority = JiraExtractors.extract_priority(row)
        status = JiraExtractors.extract_status(row)
        created = JiraExtractors.extract_created(row)
        updated = JiraExtractors.extract_updated(row)
        
        return {
            "key": issue_key,
            "url": issue_url,
            "summary": summary,
            "reporter": reporter,
            "priority": priority,
            "status": status,
            "created": created,
            "updated": updated
        }

    def print_issues(self, issues):
        """Print formatted list of issues."""
        JiraUtils.print_issues(issues)

    def close(self):
        """Close the scraper."""
        super().close()

    def _fetch_issue_description(self, issue_url):
        """Fetch the description from an individual issue page."""
        try:
            # Convert relative URL to absolute URL if needed
            if issue_url.startswith('/browse/'):
                full_url = f"{self.base_url}{issue_url}"
            else:
                full_url = issue_url
            
            print(f"    Fetching description from: {full_url}")
            
            # Navigate to the issue page
            self.driver.get(full_url)
            
            # Wait for the description element to load
            wait = WebDriverWait(self.driver, 10)
            
            # Try multiple selectors for the description
            description_selectors = [
                "p[data-renderer-start-pos='1']",  # Your specific selector
                "[data-testid='issue.views.issue-base.foundation.description.description-content'] p",
                ".ak-editor-content-area p",
                ".user-content-block p",
                "[data-test-id='issue-description'] p"
            ]
            
            description_text = "No description available"
            
            for selector in description_selectors:
                try:
                    desc_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    description_text = desc_element.text.strip()
                    if description_text:
                        print(f"    Found description: {description_text[:100]}...")
                        break
                except:
                    continue
            
            if description_text == "No description available":
                print("    No description found with any selector")
            
            return description_text
            
        except Exception as e:
            print(f"    Error fetching description: {e}")
            return "Error fetching description"
