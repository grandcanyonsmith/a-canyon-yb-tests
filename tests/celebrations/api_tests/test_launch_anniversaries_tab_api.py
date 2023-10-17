import requests
import pytest

URL = "https://i18napi-perf-prd.alamoapp.octanner.io/5464be5f-b704-44c7-907f-8cf6103d3f84/ccyearbook"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US",
    "cache-control": "no-cache",
    "origin": "https://cc-qa.culturecloud.com",
    "pragma": "no-cache",
    "referer": "https://cc-qa.culturecloud.com/",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

def make_request(url, headers):
    """Function to make a request to a given URL with provided headers."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

@pytest.mark.performance
def test_request_performance(benchmark):
    """Function to test the performance of the make_request function."""
    result = benchmark(make_request, URL, HEADERS)
    assert result is not None, "Request failed"