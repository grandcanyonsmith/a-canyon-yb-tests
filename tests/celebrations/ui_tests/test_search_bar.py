import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# All constants are at the top, below the imports in all caps
ENV_FILES = {
    'qa': 'env/.env.qa',
    'stg': 'env/.env.stg',
    'prod': 'env/.env.prod',
    'gam': 'env/.env.gam',
}

CURRENT_ENVIRONMENT = os.getenv('CURRENT_ENVIRONMENT', 'qa')

def load_environment_variables(environment):
    """Load environment variables from .env file based on the environment"""
    if environment not in ENV_FILES:
        raise ValueError(f"Invalid environment: {environment}")
    dotenv_path = ENV_FILES[environment]
    load_dotenv(dotenv_path)

load_environment_variables(CURRENT_ENVIRONMENT)

@pytest.mark.ui
def test_login(page: Page):
    """Test the login functionality"""
    # Define variables for better readability and maintainability
    username = os.getenv('CELEBRATIONS_USER')
    password = os.getenv('PASSWORD')
    url = os.getenv('ANNIVERSARIES_URL')

    # Navigate to the URL
    page.goto(url)
    print("Navigated to the URL")

    # Fill in the login form and submit
    fill_and_submit_login_form(page, username, password)

    # Verify successful login
    verify_successful_login(page)

    # Perform some actions
    perform_actions(page)

    # Verify successful logout
    verify_successful_logout(page)

def fill_and_submit_login_form(page: Page, username: str, password: str):
    """Fill and submit the login form"""
    page.fill('input[name="username"]', username)
    page.click('button[id="nextButton"]')
    page.fill('input[name="password"]', password)
    page.click('button[id="signInButton"]')
    print("Filled and submitted the login form")

def verify_successful_login(page: Page):
    """Verify successful login"""
    expect(page).to_have_selector('text=Anniversaries', visible=True)
    print("Verified successful login")

def perform_actions(page: Page):
    """Perform some actions after login"""
    page.type('input[id="mui-3"]', "ned")
    expect(page).to_have_selector('text=ned', visible=True)
    page.click('button[data-testid="current-user-name-header"]')
    page.click('a[data-testid="logout-link"]')
    print("Performed actions")

def verify_successful_logout(page: Page):
    """Verify successful logout"""
    expect(page).to_have_selector('text=You have been successfully logged out.', visible=True)
    print("Verified successful logout")