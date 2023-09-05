import requests
import base64
import json
import os
import time
from .const import Constants

# Get auth token using curl
# API_USER = ''
# API_PASS = ''
# AUTH_TOKEN=$(curl -k -s --user KMLz5g7fbmx8RVFKKdu0NOrJic4a:6NjRXBcFfLZOwHc0Xlidiz4ywcsa -d 'grant_type=password&username=$API_USER&password=$API_PASS&scope=sample-setup+run-design+run-qc+data-management+analysis+userinfo+openid' https://smrt.rc.byu.edu:8243/token | ~/jq -r .access_token)

# Make API call using curl and auth token
# curl -k -s -H 'Authorization: Bearer $AUTH_TOKEN' http://localhost:9091/smrt-link/project

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
        username, password = _get_userpass()
        authentication_params = _password_authentication(username, password)
        try:
            self.token, self.refresh_token, token_seconds = _get_tokens(authentication_params)
            self.token_expiration = time.time() + token_seconds
        except Exception as e:
            print('Failed to get token: ' + str(e))
            exit(1)
    
    def _refresh_token(self):
        authentication_params = _refresh_authentication(self.refresh_token)
        try:
            self.token, self.refresh_token, token_seconds = _get_tokens(authentication_params)
            self.token_expiration = time.time() + token_seconds
        except Exception as e:
            print('Failed to refresh token: ' + str(e))
            exit(1)

    def get_token(self):
        if time.time() >= self.token_expiration:
            self._refresh_token()
        return self.token

def _password_authentication(username, password):
    # dictionary of authentication parameters
    return dict(grant_type='password',
                username=username,
                password=password,
                scope=Constants.SCOPE)

def _refresh_authentication(refresh_token):
    # dictionary of authentication parameters
    return dict(grant_type='refresh_token',
                refresh_token=refresh_token,
                scope=Constants.SCOPE)

def _get_authorization():
    secret = 'KMLz5g7fbmx8RVFKKdu0NOrJic4a' 
    consumer_key = '6NjRXBcFfLZOwHc0Xlidiz4ywcsa' 
    return base64.b64encode(':'.join([secret, consumer_key]).encode('utf-8')).decode('utf-8')

AUTHORIZATION = _get_authorization()

def _request_token(payload):
    headers = {
        'Authorization': f'Basic {AUTHORIZATION}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # verify is false to disable the SSL cert verification
    return requests.post(Constants.TOKEN_URL, payload, headers=headers, verify=False)

def _get_tokens(authentication_params):
    r = _request_token(authentication_params)
    try:
        r.raise_for_status()
    except Exception as e:
        print('Authentication failed: ' + str(e))
        exit(1)
    j = r.json()
    access_token = j['access_token']
    refresh_token = j['refresh_token']
    expires_in_sec = j['expires_in']
    return access_token, refresh_token, expires_in_sec

def _get_userpass():
    # returns two strings: username, password
    username = os.environ['USER']
    password = None
    try:
        if username == 'dnascapp':
            password = _read_password()
        else:
            password = _prompt_user_for_password(username)
    except Exception as e:
        print('Failed to get username and password: ' + str(e))
        exit(1)
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