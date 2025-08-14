#  Add the parent directory to sys.path so imports work
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.jira import JiraScraper
from config import settings
from scraper.confluence_scraper import ConfluenceScraper

def run_all():
    jira = JiraScraper()  
    
    try:
        issues = jira.scrape()
        jira.print_issues(issues)
    finally:
        jira.close()
 

    # confluence = ConfluenceScraper(base_url=settings.CONFLUENCE_URL, headless=settings.HEADLESS)
    # try:
    #     confluence.login(username=settings.CONFLUENCE_USERNAME, password=settings.CONFLUENCE_PASSWORD)
    #     confluence.scrape()
    # finally:
    #     # jira.close()
    #     confluence.close()

if __name__ == "__main__":
    run_all()
