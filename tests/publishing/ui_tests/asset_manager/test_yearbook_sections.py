import pytest
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
import random

ENV_FILES = {
    'qa': 'env/.env.qa',
    'stg': 'env/.env.stg',
    'prod': 'env/.env.prod',
    'gam': 'env/.env.gam',
}

YEARBOOK_SECTIONS = {
    "Award Level Message": "award-level-message",
    "Executive Message": "executive-message",
    "Brand Message": "brand-message",
    "Symbol Message": "symbol-message",
    "Order Instructions": "order-instructions",
    "Leader Personal Note": "leader-personal-note",
    "Peer Personal Notes": "peer-personal-notes",
    "Welcome": "welcome",
}

def load_environment_variables(current_environment='qa'):
    if current_environment not in ENV_FILES:
        raise ValueError(f"Invalid environment: {current_environment}")
    dotenv_path = ENV_FILES[current_environment]
    load_dotenv(dotenv_path)

def sign_in(page):
    page.locator('id=usernameField').fill(os.environ['USERNAME'])
    page.locator('id=nextButton').click()
    page.locator('id=passwordField').fill(os.environ['PASSWORD'])
    page.locator('id=signInButton').click()

def random_yearbook_section():
    return random.choice(list(YEARBOOK_SECTIONS.keys()))

def navigate_to_yearbook_template(page: Page, template_id: str):
    page.goto(os.environ['MEDIA_LIBRARY_URL'])
    sign_in(page)
    page.locator('data-testid=client-search').fill("YB Publishing Automation")
    page.locator(f'data-testid=client:{os.environ["YEARBOOK_PUBLISHING_AUTOMATION_CLIENT_UUID"]}').click()
    page.locator(f'data-testid=program:{os.environ["YEARBOOK_PUBLISHING_SECTIONS_PROGRAM_UUID"]}').click()
    page.locator(f'data-testid=version-card:{template_id}').click()

def test_yearbook_sections(page: Page, template_id: str, handler_id: str):
    load_environment_variables()
    navigate_to_yearbook_template(page, template_id)
    random_section_title = random_yearbook_section()
    page.locator(f'data-testid=sectionsColumn:available:{YEARBOOK_SECTIONS[random_section_title]}').drag_to(page.locator(f'[data-handler-id={handler_id}]'))
    expect(page.locator('data-testid=sectionsColumn:yearbook')).to_contain_text(random_section_title)
    page.get_by_text(random_section_title, exact=True).drag_to(target=page.locator('[data-handler-id=T0]'))
    expect(page.locator('data-testid=sectionsColumn:available')).to_contain_text(random_section_title)

@pytest.mark.ui
def test_printed_yearbook_sections(page: Page):
    test_yearbook_sections(page, os.environ["YEARBOOK_PUBLISHING_PRINTED_SECTIONS_TEMPLATE_ID"], 'T3')

@pytest.mark.ui
def test_digital_yearbook_sections(page: Page):
    test_yearbook_sections(page, os.environ["YEARBOOK_PUBLISHING_DIGITAL_SECTIONS_TEMPLATE_ID"], 'T1')