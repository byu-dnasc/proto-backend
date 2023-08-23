from auth import TokenManager
from get import get_status, get_projects
import urllib3
import json

# _get_services_ep method in get.py uses requests.get(verify=False), therefore disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == '__main__':

    # any tasks requiring multiple should receive the token manager, not the token
    token_manager = TokenManager() 

    token = token_manager.get_token()

    print(json.dumps(get_status(token), indent=4, sort_keys=True))
    print(json.dumps(get_projects(token), indent=4, sort_keys=True))
