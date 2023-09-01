from smrtlink.client import SmrtClient
from globus.transfer import get_transfer_client
from globus.auth import get_authorizer
import json

def get_smrt_client():
    smrtc = None
    try:
        smrtc = SmrtClient()
    except Exception as e:
        print(e)
        exit(1)
    return smrtc

def main():

    smrt_client = get_smrt_client()
    if smrt_client is not None:
        pass
        # do stuff
    
    # read ccsreads.json
    ccsreads = None
    with open('ccsreads.json', 'r') as f:
        ccsreads = json.load(f)
    
    authorizer = get_authorizer()
    tc = get_transfer_client(authorizer)

    
if __name__ == '__main__':
    main()