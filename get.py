import requests
from const import Constants

def _to_headers(access_token):
    return {
    "Authorization": "Bearer {}".format(access_token),
    "Content-type": "application/json" }

def _get_services_ep(api_path, access_token):
    api_url = Constants.SERVICES_EP_BASE + api_path
    headers = _to_headers(access_token)
    # verify=False disables SSL verification
    response = requests.get(api_url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_status(access_token):
    # note: status URL is on a different endpoint than the other services
    headers = _to_headers(access_token)
    response = requests.get(Constants.STATUS_URL, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_projects(access_token):
    return _get_services_ep("/projects", access_token)