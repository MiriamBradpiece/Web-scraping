"""Jira field extraction utilities - compact version."""

from selenium.webdriver.common.by import By
import re


class JiraExtractors:
    """Handles extraction of various fields from Jira issue rows."""
    
    @staticmethod
    def _try_selectors(row, selectors):
        """Try multiple selectors, return first match."""
        for selector in selectors:
            try:
                return row.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                continue
        return None
    
    @staticmethod
    def extract_issue_key(row, row_number):
        """Extract issue key and URL from row."""
        for selector in ["a[href*='/browse/']", ".issue-link", "[data-testid*='issue-key']"]:
            try:
                el = row.find_element(By.CSS_SELECTOR, selector)
                key, url = el.text.strip(), el.get_attribute("href")
                if key and url:
                    return key, url
            except:
                continue
        return None

    @staticmethod
    def extract_summary(row):
        """Extract issue summary from row."""
        selectors = ["[data-testid*='summary']", ".summary", ".issue-summary"]
        return JiraExtractors._try_selectors(row, selectors) or "N/A"

    @staticmethod
    def extract_reporter(row, row_number):
        """Extract reporter name from row."""
        # Try aria-label first
        for selector, attr in [("button[aria-label*='edit Reporter']", "aria-label"), 
                               ("span[aria-label*='More information about']", "aria-label")]:
            try:
                text = row.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
                clean = text.replace('- edit Reporter', '').replace('More information about', '').strip()
                if clean and clean.lower() != "unassigned":
                    return clean
            except:
                continue
        
        # Try text selectors
        result = JiraExtractors._try_selectors(row, ["span[hidden]", "span._1reo15vq span", "[data-vc='profilecard-wrapper-ssr'] span"])
        return result if result and result.lower() != "unassigned" else "N/A"

    @staticmethod
    def extract_priority(row):
        """Extract priority from row."""
        return JiraExtractors._try_selectors(row, ["span._1reo15vq._18m915vq._18u0u2gc", ".priority", "[data-testid*='priority']"]) or "N/A"

    @staticmethod
    def extract_status(row):
        """Extract status from row."""
        result = JiraExtractors._try_selectors(row, ["span._1reo15vq div._4cvr1h6o", ".status span", "[data-testid*='status'] span"])
        return result.split('\n')[0] if result else "N/A"

    @staticmethod
    def extract_created(row):
        """Extract creation date from row."""
        # Try Edit Created containers
        try:
            for container in row.find_elements(By.CSS_SELECTOR, "[data-testid='issue-field-inline-edit-read-view-container.ui.container']"):
                try:
                    container.find_element(By.CSS_SELECTOR, "button[aria-label='Edit Created']")
                    date = re.search(r'[A-Za-z]{3}\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\s+[AP]M', container.text)
                    if date:
                        return date.group(0)
                except:
                    continue
        except:
            pass
        
        # Fallback: first date in row
        dates = re.findall(r'[A-Za-z]{3}\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\s+[AP]M', row.text)
        return dates[0] if dates else "N/A"

    @staticmethod
    def extract_updated(row):
        """Extract last updated date from row."""
        # Try Edit Updated containers
        try:
            for container in row.find_elements(By.CSS_SELECTOR, "[data-testid='issue-field-inline-edit-read-view-container.ui.container']"):
                try:
                    container.find_element(By.CSS_SELECTOR, "button[aria-label='Edit Updated']")
                    date = re.search(r'[A-Za-z]{3}\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\s+[AP]M', container.text)
                    if date:
                        return date.group(0)
                except:
                    continue
        except:
            pass
        
        # Fallback: second date or first date in row
        dates = re.findall(r'[A-Za-z]{3}\s+\d{1,2},\s+\d{4},\s+\d{1,2}:\d{2}\s+[AP]M', row.text)
        return dates[1] if len(dates) > 1 else (dates[0] if dates else "N/A")
