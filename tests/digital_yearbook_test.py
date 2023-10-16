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
        yield browser.new_page()
        browser.close()

def login_to_culture_cloud(page, url, username, password):
    """Login to Culture Cloud with given credentials."""
    page.goto(url)
    page.fill('#usernameField', username)
    page.click('#nextButton')
    page.fill('#passwordField', password)
    page.click('#signInButton')
    assert page.url == url

@pytest.mark.parametrize("url, username, password", [(env.get('CULTURE_CLOUD_URL'), env.get("AUTOMATION_USERNAME"), env.get('AUTOMATION_USER_PASSWORD'))])
def test_login_to_culture_cloud(browser, url, username, password):
    """Test the login functionality of Culture Cloud."""
    login_to_culture_cloud(browser, url, username, password)