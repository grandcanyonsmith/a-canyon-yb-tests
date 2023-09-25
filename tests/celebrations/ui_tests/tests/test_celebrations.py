import logging
import os
import pytest

from dotenv import load_dotenv
from testrail import testrail_helper as tr
from playwright.sync_api import sync_playwright

load_dotenv()

base_url = 'https://octanner.testrail.io'
username = os.getenv('TESTRAIL_USERNAME')
password = os.getenv('TESTRAIL_PASSWORD')
project_id = 33
suite_id = 2775
run_name = 'Automated Celebrations Health Check 9/15'

SELECTORS = {
    "username_field": "id=usernameField",
    "password_field": "id=passwordField",
    "next_button": "id=nextButton",
    "signin_button": "id=signInButton",
}

# Logger
logger = logging.getLogger(__name__)

class LoginPage:
    """
    Class representing the login page. It contains methods to interact with the login page.

    :param page: The page object from playwright
    """

    def __init__(self, page):
        self._page = page

    def login_to_page(self):
        """
        Logs into the page by filling the username and password fields and clicking the next and sign in buttons.

        :return: None
        """
        self._page.goto(os.getenv('CELEBRATIONS_URL_QA'))
        self._fill_field_and_click_button(
            SELECTORS["username_field"],
            os.getenv('CC_USERNAME'),
            SELECTORS["next_button"],
        )

        self._fill_field_and_click_button(
            SELECTORS["password_field"],
            os.getenv('CC_USER_PASSWORD'),
            SELECTORS["signin_button"],
        )

    def _fill_field_and_click_button(self, fill_selector, fill_value, click_selector):
        """
        Fills a field specified by fill_selector with fill_value and clicks a button specified by click_selector.

        :param fill_selector: The selector of the field to fill
        :param fill_value: The value to fill the field with
        :param click_selector: The selector of the button to click
        :return: None
        """
        try:
            self._page.fill(fill_selector, fill_value)
            self._page.click(click_selector)
        except Exception as e:
            logger.error(
                f"Failed to fill {fill_selector} or click {click_selector}: {str(e)}"
            )
            raise


class AnniversaryPage:
    """
    Class representing the anniversary page. It contains methods to interact with the anniversary page.

    :param page: The page object from playwright
    """

    def __init__(self, page):
        self._page = page

    def validate_personal_notes(self):
        """
        Tests the personal notes functionality on the anniversary page.

        :return: "Success" if the test passes
        """
        self._page.click("text=Anniversaries")
        self._page.click('css=[data-testid="celebrationCard"]:nth-child(2) [data-testid="writeButton"]')
        self._page.click("id=mui-4")
        self._page.keyboard.press("Control+Shift+A")
        self._page.keyboard.press("Delete")
        self._page.fill("id=mui-4", "Test the personal note modal with text")
        self._page.click("data-testid=modal-preview-button")
        self._page.click("data-testid=modal-save-button")
        self._page.click("data-testid=notes-modal-button-done")
        return "Success"

    def validate_profile(self):
        """
        Tests the profile functionality on the anniversary page.

        :return: "Success" if the test passes
        """
        self._page.click("text=Anniversaries")
        self._page.click("data-testid=current-user-name-header")
        self._page.click("data-testid=profile-link")
        self._page.wait_for_selector("data-testid=profile-sidebar", state="visible")
        self._page.wait_for_selector("text=Reports to", state="visible")
        return "Success"


@pytest.fixture(scope="module")
def browser_page():
    """
    Pytest fixture that sets up and tears down a page for testing.

    :return: A new page object from playwright
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser.new_page()
        browser.close()


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown(browser_page):
    """
    Pytest fixture that sets up and tears down a login page for testing.

    :param browser_page: The page object from playwright
    :return: None
    """
    LoginPage(browser_page).login_to_page()
    yield
    browser_page.close()


def test_login(browser_page):
    """
    Test function that tests the login functionality.

    :param browser_page: The page object from playwright
    :return: None
    """
    LoginPage(browser_page).login_to_page()


def test_anniversary_page(browser_page):
    """
    Test function that tests the anniversary page functionality.

    :param browser_page: The page object from playwright
    :return: None
    """
    anniversary_page = AnniversaryPage(browser_page)

    try:
        case_id = 232306
        test_status = '1' if anniversary_page.validate_personal_notes() == "Success" else '5'
        tr.upload_test_result_to_testrail(base_url, username, password, os.getenv("test_run_id"), case_id, test_status)
    except Exception as e:
        print(f"An error occurred while uploading the test result: {str(e)}")

    try:
        case_id = 232312
        test_status = '1' if anniversary_page.validate_profile() == "Success" else '5'
        tr.upload_test_result_to_testrail(base_url, username, password, os.getenv("test_run_id"), case_id, test_status)
    except Exception as e:
        print(f"An error occurred while uploading the test result: {str(e)}")

