import requests

from smrtlink.const import Constants

def _get_url(api_path):
    api_url = Constants.SERVICES_EP_BASE + api_path
    if api_path == '/status':
        # status URL is on a different endpoint than the other services
        api_url = Constants.STATUS_URL
    return api_url

def _get_headers(access_token):
    if access_token is None:
        return None
    return {
        'Authorization': 'Bearer ' + access_token,
        'Content-type': 'application/json' 
    }

def post_endpoint(api_path, access_token, data):
    try:
        try:
            response = requests.post(
                url=_get_url(api_path), 
                headers=_get_headers(access_token), 
                json=data, 
                verify=False # causes warnings from urllib3. 
            )
        except requests.exceptions.ConnectionError:
            raise Exception('Could not connect to SMRT Link server')
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception('SMRTLink response not OK: ' + str(e))
    except Exception as e:
        raise Exception('SmrtClient failed to post endpoint: ' + str(e))
    return response.json()
 
def get_endpoint(api_path, access_token):
    try:
        try:
            response = requests.get(
                url=_get_url(api_path), 
                headers=_get_headers(access_token), 
                verify=False # causes warnings from urllib3. 
            )
        except requests.exceptions.ConnectionError:
            raise Exception('Could not connect to SMRT Link server')
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception('SMRTLink response not OK: ' + str(e))
    except Exception as e:
        raise Exception('SmrtClient failed to get endpoint: ' + str(e))
    return response.json()

