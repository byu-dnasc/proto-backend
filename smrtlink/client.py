from .const import Constants
from .auth import TokenManager
import requests
import urllib3

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
 
def _get_endpoint(api_path, access_token):
    try:
        response = requests.get(url=_get_url(api_path), 
                                headers=_get_headers(access_token), 
                                verify=False)
        # verify=False causes warnings from urllib3. 
        # warnings are disabled by SmrtClient.__init__
    except requests.exceptions.ConnectionError:
        raise Exception('Could not connect to SMRT Link server')
    response.raise_for_status()
    return response.json()

class SmrtClient:

    def __init__(self):
        # verify that the server is accessible
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # see _get_endpoint
        try: 
            self.get_status()
        except Exception as e:
            raise Exception('Failed to create SmrtClient: ' + str(e))
        # initialize
        try:
            self.token_manager = TokenManager()
        except Exception as e:
            raise Exception('Failed to create SmrtClient: ' + str(e))

    def _get_token(self):
        return self.token_manager.get_token()
    
    def get_user(self):
        return _get_endpoint('/user', self._get_token())
    
    def get_projects(self):
        return _get_endpoint('/projects', self._get_token())
    
    def get_status(self):
        return _get_endpoint('/status', None)
    
    def get_dataset_by_id(self, dataset_id):
        # dataset_id could be the uuid or the id
        return _get_endpoint(f'/datasets/search/{dataset_id}', self._get_token())
    
    def get_ccsreads(self):
        return _get_endpoint('/datasets/ccsreads', self._get_token())

    def get_subreads(self):
        return _get_endpoint('/datasets/subreads', self._get_token())
    
    def get_dataset_reports(self, dataset_id):
        return _get_endpoint(f'/datasets/ccsreads/{dataset_id}/reports', self._get_token())

    def import_fastx(self, file_path):
        # Upon further examination, is think this is the API
        # for uploading files to the SMRT Link server from
        # the UI. Probably only useful for that. Tried it on
        # smrt.rc.byu.edu and it didn't work.
        '''
        -bash-4.2$ curl -X POST "https://localhost:9091/smrt-link/uploader" \
        > -H "accept: application/json" \
        > -H "Content-Type: application/json" \
        > -d '{"path":"/home/aknaupp/example.fastq"}'
        curl: (35) SSL received a record that exceeded the maximum permissible length.
        -bash-4.2$
        '''
        # maybe means that the response was HTML?
        api_url = Constants.SERVICES_EP_BASE + '/uploader'
        payload = { 'path': file_path }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(api_url, headers=headers, data=payload, verify=False)