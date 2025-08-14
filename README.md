# Jira Web Scraper (Selenium + OOP)

This project is an **efficient, object-oriented** Python tool for scraping Jira issue data using Selenium WebDriver.  
It is designed with **clean OOP principles** for better maintainability, reusability, and scalability.

## Features
- **Object-Oriented Design** for clear code structure
- Automated login to Jira
- Support for **custom JQL filters**
- Handles pagination & dynamic elements
- Optional **headless mode** for background execution

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following:

   **Example `.env`**
   ```env
   JIRA_URL=https://myk04052004.atlassian.net/jira/software/projects/PROJECT_KEY/boards/BOARD_ID
   LOGIN_URL=https://id.atlassian.com/login?continue=https%3A%2F%2Fmyk04052004.atlassian.net

   JIRA_USERNAME=your.email@example.com
   JIRA_PASSWORD=yourSecurePassword123

   HEADLESS=false # set to true to run without opening the browser
   ```

## Usage
Run the scraper:
```bash
python main.py
```

## Tech Stack
- Python
- Selenium WebDriver
- `python-dotenv` for environment variables

## Notes
- Make sure your Jira credentials are correct and your account has access to the issues you want to scrape.
- The `.env` file should **never** be committed to GitHub — it's already ignored via `.gitignore`.
