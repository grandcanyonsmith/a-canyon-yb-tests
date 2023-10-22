import os
from dotenv import load_dotenv
import pytest
from testrail import testrail_helper as tr
from playwright.sync_api import sync_playwright

# Constants
BASE_URL = 'https://octanner.testrail.io'
USERNAME = os.getenv('TESTRAIL_USERNAME')
PASSWORD = os.getenv('TESTRAIL_PASSWORD')
PROJECT_ID = 33
SUITE_ID = 2775
RUN_NAME = 'Automated Celebrations Health Check'

load_dotenv()

def create_test_run():
    """
    Create a test run and set the id in the environment variables
    """
    test_run_id = tr.create_test_run(BASE_URL, USERNAME, PASSWORD, PROJECT_ID, SUITE_ID, RUN_NAME)
    os.environ["test_run_id"] = f"{test_run_id}"
    print("Test run created with id: ", test_run_id)

def close_test_run():
    """
    Close the test run
    """
    tr.close_test_run(os.getenv("test_run_id"), BASE_URL, USERNAME, PASSWORD)
    print("Test run closed")

@pytest.fixture(scope='session', autouse=True)
def run_tests():
    """
    Setup and teardown for tests
    """
    print("Setting up tests")
    create_test_run()
    yield
    print("Tearing down tests")
    close_test_run()