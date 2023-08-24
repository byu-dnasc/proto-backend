from auth import TokenManager
from client import SmrtClient
import urllib3
import json

# get_endpoint method in smrtlink.client uses requests.get(verify=False), therefore disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == '__main__':

    # any tasks requiring multiple should receive the token manager, not the token
    token_manager = TokenManager() 

    smrtc = SmrtClient(token_manager)

    print(json.dumps(smrtc.get_status(), indent=4, sort_keys=True))