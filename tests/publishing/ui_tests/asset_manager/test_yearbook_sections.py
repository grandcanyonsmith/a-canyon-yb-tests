import pytest
from playwright.sync_api import Page, expect
import os
from dotenv import load_dotenv
import random

env_files = {
    'qa': 'env/.env.qa',
    'stg': 'env/.env.stg',
    'prod': 'env/.env.prod',
    'gam': 'env/.env.gam',
}

current_environment = 'qa'

if current_environment not in env_files:
    raise ValueError(f"Invalid environment: {current_environment}")
dotenv_path = env_files[current_environment]
load_dotenv(dotenv_path)


def sign_in(page):
    """
    Function to sign in to the page
    """
    page.locator('id=usernameField').fill(os.environ['USERNAME'])
    page.locator('id=nextButton').click()
    page.locator('id=passwordField').fill(os.environ['PASSWORD'])
    page.locator('id=signInButton').click()


yearbook_sections = {
    "Award Level Message": "award-level-message",
    "Executive Message": "executive-message",
    "Brand Message": "brand-message",
    "Symbol Message": "symbol-message",
    "Order Instructions": "order-instructions",
    "Leader Personal Note": "leader-personal-note",
    "Peer Personal Notes": "peer-personal-notes",
    "Welcome": "welcome",
    }


def random_yearbook_section():
    """
    Function to return a random yearbook section
    """
    section_list = list(yearbook_sections.keys())
    return random.choice(section_list)


@pytest.mark.ui
def test_printed_yearbook_sections(page: Page):
    """
    Function to test adding and removing sections to the printed yearbook template
    """
    page.goto(os.environ['MEDIA_LIBRARY_URL'])
    sign_in(page)
    page.locator('data-testid=client-search').fill("YB Publishing Automation")
    page.locator(f'data-testid=client:{os.environ["YEARBOOK_PUBLISHING_AUTOMATION_CLIENT_UUID"]}').click()
    page.locator(f'data-testid=program:{os.environ["YEARBOOK_PUBLISHING_SECTIONS_PROGRAM_UUID"]}').click()
    page.locator(f'data-testid=version-card:{os.environ["YEARBOOK_PUBLISHING_PRINTED_SECTIONS_TEMPLATE_ID"]}').click()
    random_section_title = random_yearbook_section()
    page.locator(f'data-testid=sectionsColumn:available:{yearbook_sections[random_section_title]}').drag_to(page.locator('[data-handler-id=T3]'))
    expect(page.locator('data-testid=sectionsColumn:yearbook')).to_contain_text(random_section_title)
    page.get_by_text(random_section_title, exact=True).drag_to(target=page.locator('[data-handler-id=T0]'))
    expect(page.locator('data-testid=sectionsColumn:available')).to_contain_text(random_section_title)


@pytest.mark.ui
def test_digital_yearbook_sections(page: Page):
    """
    Function to test adding and removing sections to the digital yearbook template
    """
    page.goto(os.environ['MEDIA_LIBRARY_URL'])
    sign_in(page)
    page.locator('data-testid=client-search').fill("YB Publishing Automation")
    page.locator(f'data-testid=client:{os.environ["YEARBOOK_PUBLISHING_AUTOMATION_CLIENT_UUID"]}').click()
    page.locator(f'data-testid=program:{os.environ["YEARBOOK_PUBLISHING_SECTIONS_PROGRAM_UUID"]}').click()
    page.locator(f'data-testid=version-card:{os.environ["YEARBOOK_PUBLISHING_DIGITAL_SECTIONS_TEMPLATE_ID"]}').click()
    random_section_title = random_yearbook_section()
    page.locator(f'data-testid=sectionsColumn:available:{yearbook_sections[random_section_title]}').drag_to(page.locator('[data-handler-id=T1]'))
    expect(page.locator('data-testid=sectionsColumn:yearbook')).to_contain_text(random_section_title)
    page.get_by_text(random_section_title, exact=True).drag_to(target=page.locator('[data-handler-id=T0]'))
    expect(page.locator('data-testid=sectionsColumn:available')).to_contain_text(random_section_title)