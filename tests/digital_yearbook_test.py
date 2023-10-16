import pytest
from dotenv import load_dotenv
from os import environ as env
from selenium.webdriver import Chrome

load_dotenv()

@pytest.fixture(scope="session")
def browser():
    driver = Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def login_to_culture_cloud(browser, url, username, password):
    browser.get(url)
    browser.find_element('id', 'usernameField').send_keys(username)
    browser.find_element('id', "nextButton").click()
    browser.find_element('id', "passwordField").send_keys(password)
    browser.find_element('id', "signInButton").click()

def test_login_to_culture_cloud(browser):
    login_to_culture_cloud(browser, env['CULTURE_CLOUD_URL'], env["AUTOMATION_USERNAME"], env['AUTOMATION_USER_PASSWORD'])