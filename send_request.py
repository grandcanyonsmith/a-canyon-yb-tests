import requests
import json

def send_post_request():
    url = 'https://nyk43gzspnm7wfhwqrc4uaprya0ecdap.lambda-url.us-west-2.on.aws/'
    data = {'request': 'update_code_in_ec2'}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ('Http Error:',errh)
    except requests.exceptions.ConnectionError as errc:
        print ('Error Connecting:',errc)
    except requests.exceptions.Timeout as errt:
        print ('Timeout Error:',errt)
    except requests.exceptions.RequestException as err:
        print ('Something went wrong',err)
    else:
        print(response.json())

send_post_request()
