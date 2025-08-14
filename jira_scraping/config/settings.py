import os
from dotenv import load_dotenv

# Absolute path to the .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes to RAG-scraping
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

JIRA_URL = os.getenv("JIRA_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

