import os
import pytest
from playwright.sync_api import sync_playwright
from testrail import testrail_helper as tr
from dotenv import load_dotenv
from utils import browser, page

class TestManagerInvite:
    """Class to test manager invite functionality"""
    def __init__(self):
        self.BASE_URL = 'https://octanner.testrail.io'
        self.USERNAME = os.getenv('TESTRAIL_USERNAME')
        self.PASSWORD = os.getenv('TESTRAIL_PASSWORD')
        self.PROJECT_ID = 33
        self.SUITE_ID = 3082
        self.RUN_NAME = 'Automated Legacy Smoke Tests'
        self.MAIN_URL = "https://vision-qa.appreciatehub.com/ui/yearbook/comment/invites/L2FwaS9wZWVyL2xlYWRlci9pbnZpdGVzLzU2NmRkMGIyNjUyM2U0MWUyOWRiNGE1Mzk2ZTA1YjRhOGFmMGM4NjU?locale=en_US"
        self.COMMENT = "Johnny has been a great asset to our team. His dedication and hard work is truly appreciated."
        self.NAME = "Canyon Smith"
        self.SELECTORS = {
            "COMMENT_LINK": "#write-comment",
            "NAME_INPUT": "#comment-name",
            "COMMENT_TEXTAREA": "#comment-comment",
            "PREVIEW_COMMENT_BUTTON": "button:has-text('Preview Comment')",
            "SUBMIT_COMMENT_BUTTON": "button:has-text('Submit Comment')",
            "POPUP_MODAL": "div.modal",
        }

    def navigate_to_main_page(self, page):
        """Navigate to main page"""
        page.goto(self.MAIN_URL)
        print("Navigated to main page")

    def write_comment_to_yearbook(self, page, comment):
        """Write a comment to a yearbook"""
        page.click(self.SELECTORS["COMMENT_LINK"])
        print("Clicked on comment link")
        page.fill(self.SELECTORS["NAME_INPUT"], self.NAME)
        print("Filled name input")
        page.fill(self.SELECTORS["COMMENT_TEXTAREA"], comment)
        print("Filled comment textarea")
        page.click(self.SELECTORS["PREVIEW_COMMENT_BUTTON"])
        print("Clicked on preview comment button")
        assert page.wait_for_selector(self.SELECTORS["SUBMIT_COMMENT_BUTTON"])
        print("Submit comment button is visible")
        page.click(self.SELECTORS["SUBMIT_COMMENT_BUTTON"])
        print("Clicked on submit comment button")
        return "Success"

    def close_popup_if_open(self, page):
        """Close the popup modal if it's open"""
        if page.is_visible(self.SELECTORS["POPUP_MODAL"]):
            page.click(self.SELECTORS["POPUP_MODAL"])
            print("Closed popup modal")

    def test_manager_invite_functionality(self, page):
        """Test manager invite functionality"""
        self.navigate_to_main_page(page)
        self.write_comment_to_yearbook(page, self.COMMENT)
        test_run_id = tr.create_test_run(self.BASE_URL, self.USERNAME, self.PASSWORD, self.PROJECT_ID, self.SUITE_ID, self.RUN_NAME)
        case_id = 249861
        try:
            test_status = '1' if self.write_comment_to_yearbook(page, self.COMMENT) == "Success" else '5'
            tr.upload_test_result_to_testrail(self.BASE_URL, self.USERNAME, self.PASSWORD, test_run_id, case_id, test_status)
            print("Uploaded test result to testrail")
        except Exception as e:
            print(f"An error occurred while uploading the test result: {str(e)}")

if __name__ == "__main__":
    test_manager_invite = TestManagerInvite()
    pytest.main(["-v", "-s", __file__])