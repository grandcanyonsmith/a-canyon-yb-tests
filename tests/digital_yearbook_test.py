import pytest
from dotenv import load_dotenv
from os import environ as env
from playwright.sync_api import sync_playwright

load_dotenv()

@pytest.fixture(scope="session")
def browser():
    """Setup and teardown for browser."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()

def login_to_culture_cloud(page, url, username, password):
    """Login to Culture Cloud with given credentials."""
    page.goto(url)
    page.fill('#usernameField', username)
    page.click('#nextButton')
    page.fill('#passwordField', password)
    page.click('#signInButton')

def test_login_to_culture_cloud(browser):
    """Test the login functionality of Culture Cloud."""
    login_to_culture_cloud(browser, env['CULTURE_CLOUD_URL'], env["AUTOMATION_USERNAME"], env['AUTOMATION_USER_PASSWORD'])