import globus_sdk
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
        # get projects
        projects = smrt_client.get_projects()
        # pretty print
        print(json.dumps(projects, indent=4))
        pass
        # do stuff
    '''
    authorizer = get_authorizer()
    globus_sc = globus_sdk.SearchClient(authorizer=authorizer)
    r = globus_sc.create_index('dnasc')
    print(r['id'])
    '''

    
if __name__ == '__main__':
    main()