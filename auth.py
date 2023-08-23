import requests
import base64
import json
import os
import time
from const import Constants

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
            cls.token = None
        return cls._instance

    def _get_new_token(self):
        # I am ignoring SMRT Link's refresh token feature for now.
        username, password = _get_userpass()
        self.token, token_seconds = _get_smrtlink_auth_token(username, password)
        self.token_expiry = time.time() + token_seconds

    def get_token(self):
        if self.token is None or time.time() >= self.token_expiry:
            self._get_new_token()
        return self.token

def _create_auth(secret, consumer_key):
    return base64.b64encode(":".join([secret, consumer_key]).encode("utf-8"))

def _get_token(url, user, password):
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

def _get_smrtlink_auth_token(username, password):
    r = _get_token(Constants.TOKEN_URL, username, password)
    r.raise_for_status()
    j = r.json()
    access_token = j['access_token']
    expires_in = j['expires_in']
    return access_token, expires_in

def _get_userpass():
    # TODO: is the app user really pacbiodnaseq? 
    # user is either pacbiodnaseq or the current user. All users should
    # already be SMRT Link users
    username = os.environ['USER']
    credentials = None
    if username == 'pacbiodnaseq':
        with open('/home/pacbiodnaseq/credentials.json') as f:
            credentials = json.load(f)
    else: 
        # prompt for username and password
        password = input("Enter your SMRT Link password: ")
        credentials = {'username': username, 'password': password}
    if credentials is None:
        raise Exception("Could not get credentials")
    return credentials['username'], credentials['password']