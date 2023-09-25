import requests
import json


class TestRailAPIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def send_post(self, uri, data):
        headers = {
            'Content-Type': 'application/json'
        }
        auth = (self.username, self.password)
        response = requests.post(f'{self.base_url}{uri}', headers=headers, auth=auth, data=json.dumps(data))
        return response

def create_test_run(base_url, username, password, project_id, suite_id, name):

    client = TestRailAPIClient(base_url, username, password)
    endpoint = f'/index.php?/api/v2/add_run/{project_id}'

    data = {
        "suite_id": suite_id,
        "name": name,
        "include_all": True,
    }

    response = client.send_post(endpoint, data)

    if response.status_code == 200:
        run_data = json.loads(response.text)
        run_id = run_data['id']
        print(f"Test Run '{name}' created successfully with ID {run_id}.")
        return run_id
    else:
        print(f"Failed to create the test run. Status code: {response.status_code}")
        print(response.text)
        return None

def upload_test_result_to_testrail(base_url, username, password, test_run_id, case_id, status_id, comment=None):

    client = TestRailAPIClient(base_url, username, password)
    endpoint = f'/index.php?/api/v2/add_result_for_case/{test_run_id}/{case_id}'

    data = {
        'status_id': status_id,
        'comment': comment
    }

    response = client.send_post(endpoint, data)

    if response.status_code == 200:
        print(f"Test result for Case ID {case_id} uploaded successfully.")
    else:
        print(f"Failed to upload test result for Case ID {case_id}. Status code: {response.status_code}")
        print(response.text)


def close_test_run(test_run_id, base_url, username, password):

    get_run_endpoint = f"{base_url}/index.php?/api/v2/get_run/{test_run_id}"

    headers = {'Content-Type': 'application/json'}
    auth = (username, password)

    try:

        response = requests.get(get_run_endpoint, headers=headers, auth=auth)

        if response.status_code == 200:
            run_data = response.json()

            all_tests_passed = run_data["failed_count"] == 0 and run_data["untested_count"] == 0

            data = {
                "include_all": True,
                "is_completed": True,
                "passed": all_tests_passed
            }

            update_endpoint = f"{base_url}/index.php?/api/v2/close_run/{test_run_id}"

            response = requests.post(update_endpoint, json=data, headers=headers, auth=auth)

            if response.status_code == 200:
                print(f"Test run with ID {test_run_id} has been closed.")
            else:
                print(f"Failed to close test run with ID {test_run_id}. Status code: {response.status_code}")
        else:
            print(f"Failed to fetch test run details. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")