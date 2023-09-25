import pytest
import re

from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv

env_files = {
    'qa': 'env/.env.qa',
    'stg': 'env/.env.stg',
    'prod': 'env/.env.prod',
    'gam': 'env/.env.gam',
}

current_environment = 'qa'

if current_environment in env_files:
    dotenv_path = env_files[current_environment]
    load_dotenv(dotenv_path)
else:
    raise ValueError(f"Invalid environment: {current_environment}")
@pytest.mark.ui
def test_login(page: Page):
    page.goto(os.environ['ANNIVERSARIES_URL'])
    page.locator('id=usernameField').fill(os.environ['CELEBRATIONS_USER'])
    page.locator('id=nextButton').click()
    page.locator('id=passwordField').fill(os.environ['PASSWORD'])
    page.locator('id=signInButton').click()

    expect(page.get_by_text("Anniversaries")).to_be_visible()

    page.locator('id=mui-3').type("ned")
    expect(page.get_by_text("ned")).to_be_visible()
    page.locator('data-testid=current-user-name-header').click()
    page.locator('data-testid=logout-link').click()
    expect(page.get_by_text("You have been successfully logged out.")).to_be_visible()
