import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

ENV_FILES = {
    'qa': 'env/.env.qa',
    'stg': 'env/.env.stg',
    'prod': 'env/.env.prod',
    'gam': 'env/.env.gam',
}

CURRENT_ENVIRONMENT = os.getenv('CURRENT_ENVIRONMENT', 'qa')

def load_environment_variables(environment):
    if environment not in ENV_FILES:
        raise ValueError(f"Invalid environment: {environment}")
    dotenv_path = ENV_FILES[environment]
    load_dotenv(dotenv_path)

load_environment_variables(CURRENT_ENVIRONMENT)

@pytest.mark.ui
def test_login(page: Page):
    # Define variables for better readability and maintainability
    username = os.getenv('CELEBRATIONS_USER')
    password = os.getenv('PASSWORD')
    url = os.getenv('ANNIVERSARIES_URL')

    # Navigate to the URL
    page.goto(url)

    # Fill in the login form and submit
    page.fill('input[name="username"]', username)
    page.click('button[id="nextButton"]')
    page.fill('input[name="password"]', password)
    page.click('button[id="signInButton"]')

    # Verify successful login
    expect(page).to_have_selector('text=Anniversaries', visible=True)

    # Perform some actions
    page.type('input[id="mui-3"]', "ned")
    expect(page).to_have_selector('text=ned', visible=True)
    page.click('button[data-testid="current-user-name-header"]')
    page.click('a[data-testid="logout-link"]')

    # Verify successful logout
    expect(page).to_have_selector('text=You have been successfully logged out.', visible=True)