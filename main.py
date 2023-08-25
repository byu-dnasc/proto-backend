from smrtlink.client import SmrtClient
from smrtlink.auth import TokenManager
import json

def main():
    token_manager = TokenManager()
    smrtc = SmrtClient(token_manager)

    # dataset 6120
    #print(json.dumps(smrtc.get_dataset_by_id('6120'), indent=4))
    print(json.dumps(smrtc.get_dataset_reports('6120'), indent=4))
    

if __name__ == '__main__':
    main()