import os
import pytest
from playwright.sync_api import sync_playwright
from testrail import testrail_helper as tr
from dotenv import load_dotenv

from utils import browser, page

load_dotenv()
# Constants
MAIN_URL = "https://vision-qa.appreciatehub.com/ui/yearbook/comment/invites/L2FwaS9wZWVyL2xlYWRlci9pbnZpdGVzLzU2NmRkMGIyNjUyM2U0MWUyOWRiNGE1Mzk2ZTA1YjRhOGFmMGM4NjU?locale=en_US"
COMMENT = "Johnny has been a great asset to our team. His dedication and hard work is truly appreciated."
NAME = "Canyon Smith"
base_url = 'https://octanner.testrail.io'
username = os.getenv('TESTRAIL_USERNAME')
password = os.getenv('TESTRAIL_PASSWORD')
project_id = 33
suite_id = 3082
run_name = 'Automated Legacy Smoke Tests'

# Selectors
SELECTORS = {
    "COMMENT_LINK": "#write-comment",
    "NAME_INPUT": "#comment-name",
    "COMMENT_TEXTAREA": "#comment-comment",
    "PREVIEW_COMMENT_BUTTON": "button:has-text('Preview Comment')",
    "SUBMIT_COMMENT_BUTTON": "button:has-text('Submit Comment')",
    "POPUP_MODAL": "div.modal",
}

def go_to_page(page):
    """Navigate to main page"""
    page.goto(MAIN_URL)

def write_comment(page, comment):
    """Write a comment to a yearbook"""
    page.click(SELECTORS["COMMENT_LINK"])
    page.fill(SELECTORS["NAME_INPUT"], NAME)
    page.fill(SELECTORS["COMMENT_TEXTAREA"], comment)
    page.click(SELECTORS["PREVIEW_COMMENT_BUTTON"])
    assert page.wait_for_selector(SELECTORS["SUBMIT_COMMENT_BUTTON"])
    page.click(SELECTORS["SUBMIT_COMMENT_BUTTON"])
    return "Success"

def close_popup(page):
    """Close the popup modal if it's open"""
    if page.is_visible(SELECTORS["POPUP_MODAL"]):
        page.click(SELECTORS["POPUP_MODAL"])

def test_manager_invites_others_to_write(page):
    """Test manager invite functionality"""
    go_to_page(page)
    write_comment(page, COMMENT)
    test_run_id = tr.create_test_run(base_url, username, password, project_id, suite_id, run_name)
    case_id = 249861
    try:
        test_status = '1' if write_comment(page, COMMENT) == "Success" else '5'
        tr.upload_test_result_to_testrail(base_url, username, password, test_run_id, case_id, test_status)
    except Exception as e:
        print(f"An error occurred while uploading the test result: {str(e)}")



if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
