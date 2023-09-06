import json
import time
from smrtlink.client import SmrtClient

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

    projects = smrt_client.get_projects()
    print(json.dumps(projects, indent=4))
    time.sleep(1801)

    projects = smrt_client.get_projects()
    print(json.dumps(projects, indent=4))
    
if __name__ == '__main__':
    main()