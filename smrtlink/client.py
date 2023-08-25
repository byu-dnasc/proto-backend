from .const import Constants
import requests
import urllib3

def _get_endpoint(api_path, access_token):
    api_url = Constants.SERVICES_EP_BASE + api_path
    if api_path == '/status':
        # status URL is on a different endpoint than the other services
        api_url = Constants.STATUS_URL
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-type': 'application/json' 
    }
    # verify=False causes warnings from urllib3. 
    # warnings are disabled elsewhere in the package
    response = requests.get(api_url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

class SmrtClient:

    def __init__(self, token_manager):
        self.token_manager = token_manager
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # see _get_endpoint
    
    def _get_token(self):
        return self.token_manager.get_token()
    
    def get_user(self):
        return _get_endpoint('/user', self._get_token())
    
    def get_projects(self):
        return _get_endpoint('/projects', self._get_token())
    
    def get_status(self):
        return _get_endpoint('/status', self._get_token())
    
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