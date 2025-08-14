"""Jira utility functions."""

from selenium.webdriver.common.by import By


class JiraUtils:
    """Utility functions for Jira scraping."""
    
    @staticmethod
    def find_issue_rows(driver):
        """Try multiple selectors to find issue rows on the page."""
        selectors_to_try = [
            "[data-testid='issue-list.ui.list-item']",  # Most specific
            "tr[data-testid*='issue']",  # Table rows
            "div[data-testid*='issue']",  # Div containers
            ".issuerow",  # Classic Jira class
            "tr.issuerow",  # Table row with class
            "a[href*='/browse/']"  # Fallback: just find all issue links
        ]

        for selector in selectors_to_try:
            try:
                potential_rows = driver.find_elements(By.CSS_SELECTOR, selector)
                if potential_rows:
                    print(f"Found {len(potential_rows)} elements with selector: {selector}")
                    return potential_rows
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                continue
        
        return []
    
    @staticmethod
    def fallback_extraction(driver):
        """Fallback method to extract basic issue information when row structure is not found."""
        print("No issue rows found with any selector. Trying direct link extraction...")
        issues = []
        
        issue_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/browse/']")
        for link in issue_links:
            try:
                issue_key = link.text.strip()
                issue_url = link.get_attribute("href")
                if issue_key and issue_url:
                    issues.append({
                        "key": issue_key,
                        "url": issue_url,
                        "summary": "Summary not available",
                        "reporter": "N/A",
                        "priority": "N/A",
                        "status": "N/A",
                        "created": "N/A",
                        "updated": "N/A",
                        "description": "Description not available"
                    })
            except Exception as e:
                print(f"Error extracting link: {e}")
                continue
        
        print(f"Found {len(issues)} issues using fallback method")
        return issues
    
    @staticmethod
    def handle_scraping_error(driver, error):
        """Handle errors that occur during scraping."""
        print(f"Error during scraping: {error}")
        print(f"Current URL: {driver.current_url}")
        screenshot_path = "scrape_error.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        return []
    
    @staticmethod
    def print_issues(issues):
        """Print formatted list of issues."""
        print("\n=== Jira Issues ===")
        for issue in issues:
            print(f"{issue['key']} | {issue['summary']}")
            print(f"  Reporter: {issue['reporter']} | Priority: {issue['priority']} | Status: {issue['status']}")
            print(f"  Created: {issue['created']} | Updated: {issue['updated']}")
            print(f"  Description: {issue.get('description', 'N/A')[:200]}...")  # Show first 200 chars
            print(f"  URL: {issue['url']}")
            print("  " + "-"*50)
