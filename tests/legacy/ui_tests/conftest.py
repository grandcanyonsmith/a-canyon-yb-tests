import os
from dotenv import load_dotenv
import pytest
from testrail import testrail_helper as tr
from playwright.sync_api import sync_playwright

load_dotenv()

BASE_URL = 'https://octanner.testrail.io'
USERNAME = os.getenv('TESTRAIL_USERNAME')
PASSWORD = os.getenv('TESTRAIL_PASSWORD')
PROJECT_ID = 33
SUITE_ID = 3082
RUN_NAME = 'Automated Legacy Smoke Tests'
TEST_RUN_ID = None

def setup_before_tests():
    """Setup before running tests."""
    global TEST_RUN_ID
    TEST_RUN_ID = tr.create_test_run(BASE_URL, USERNAME, PASSWORD, PROJECT_ID, SUITE_ID, RUN_NAME)

@pytest.fixture(scope='session', autouse=True)
def after_all_tests():
    """Teardown after running all tests."""
    setup_before_tests()
    yield

    tr.close_test_run(TEST_RUN_ID, BASE_URL, USERNAME, PASSWORD)

    print("Finished running after all tests")