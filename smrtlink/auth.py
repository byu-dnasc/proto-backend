import requests
import base64
import json
import os
import time
from .const import Constants

# Get auth token using curl
# API_USER = ''
# API_PASS = ''
# AUTH_TOKEN=$(curl -k -s --user KMLz5g7fbmx8RVFKKdu0NOrJic4a:6NjRXBcFfLZOwHc0Xlidiz4ywcsa -d "grant_type=password&username=$API_USER&password=$API_PASS&scope=sample-setup+run-design+run-qc+data-management+analysis+userinfo+openid" https://smrt.rc.byu.edu:8243/token | ~/jq -r .access_token)

# Make API call using curl and auth token
# curl -k -s -H "Authorization: Bearer $AUTH_TOKEN" http://localhost:9091/smrt-link/project

class TokenManager:
    # token manager is a singleton which maintains an up-to-date token
    _instance = None
    
    # Singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        try:
            self.username, self.password = _get_userpass()
        except Exception as e:
            print('Failed to get username and password: ' + str(e))
            exit(1)
        self.token = None

    def _get_new_token(self):
        # I am ignoring SMRT Link's refresh token feature for now.
        self.token, token_seconds = _get_smrtlink_access_token(self.username, self.password)
        self.token_expiry = time.time() + token_seconds

    def get_token(self):
        if self.token is None or time.time() >= self.token_expiry: # TODO: verify this logic
            self._get_new_token()
        return self.token

def _create_auth(secret, consumer_key):
    return base64.b64encode(":".join([secret, consumer_key]).encode("utf-8"))

def _request_token(url, user, password):
    scopes = ["welcome", "run-design", "run-qc", "openid", "analysis", "sample-setup", "data-management", "userinfo"]
    basic_auth = _create_auth("KMLz5g7fbmx8RVFKKdu0NOrJic4a", "6NjRXBcFfLZOwHc0Xlidiz4ywcsa").decode("utf-8")
    headers = {
    "Authorization": "Basic {}".format(basic_auth),
    "Content-Type": "application/x-www-form-urlencoded"
    }
    scope_str = " ".join({s for s in scopes})
    payload = dict(grant_type="password",
                   username=user,
                   password=password,
                   scope=scope_str)
    # verify is false to disable the SSL cert verification
    return requests.post(url, payload, headers=headers, verify=False)

def _get_smrtlink_access_token(username, password):
    r = _request_token(Constants.TOKEN_URL, username, password)
    try:
        r.raise_for_status()
    except Exception as e:
        print('Authentication failed: ' + str(e))
        exit(1)
    j = r.json()
    access_token = j['access_token']
    expires_in = j['expires_in']
    return access_token, expires_in

def _get_userpass():
    # returns two strings: username, password
    username = os.environ['USER']
    password = None
    if username == 'dnascapp':
        password = _read_password()
    else:
        password = _prompt_user_for_password(username)
    return username, password

def _read_password():
    e_message = 'Could not read password: '
    if os.path.isfile('/home/dnascapp/credentials.json'):
        with open('/home/dnascapp/credentials.json') as f:
            j = json.load(f)
            # check that file contains the correct key
            if 'SMRT Link Password' in j:
                return j['SMRT Link Password']
            else:
                raise Exception(e_message + '/home/dnascapp/credentials.json missing key "SMRT Link Password".')
    else:
        raise Exception(e_message + '/home/dnascapp/credentials.json does not exist.')

def _prompt_user_for_password(username):
    prompt = f'Enter the SMRT Link password for {username}, or exit and run as dnascapp: '
    password = input(prompt)
    if password == '':
        raise Exception(f'No password entered for {username}.')
    return password