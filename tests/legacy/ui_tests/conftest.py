import os

from dotenv import *
import pytest

from testrail import testrail_helper as tr
from playwright.sync_api import sync_playwright

load_dotenv()

base_url = 'https://octanner.testrail.io'
username = os.getenv('TESTRAIL_USERNAME')
password = os.getenv('TESTRAIL_PASSWORD')
project_id = 33
suite_id = 3082
run_name = 'Automated Legacy Smoke Tests'

def setup_before_tests():
    """Setup before running tests."""
    test_run_id = tr.create_test_run(base_url, username, password, project_id, suite_id, run_name)
    os.environ["test_run_id"] = f"{test_run_id}"
    pass

@pytest.fixture(scope='session', autouse=True)
def after_all_tests():
    """Teardown after running all tests."""
    setup_before_tests()
    yield

    tr.close_test_run(os.getenv("test_run_id"), base_url, username, password)

    print("Finished running after all tests")
#END