#  Add the parent directory to sys.path so imports work
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.jira_scraper import JiraScraper
from config import settings
# from scraper.confluence_scraper import ConfluenceScraper

def run_all():
    jira = JiraScraper()  
    
    try:
        issues = jira.scrape()
        jira.print_issues(issues)
    finally:
        jira.close()
 


if __name__ == "__main__":
    run_all()
