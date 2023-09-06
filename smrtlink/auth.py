import requests
import base64
import json
import os
import time
import getpass
from .const import Constants

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
        # get tokens, handle invalid passwords
        while True:
            try:
                username, password = _get_userpass()
                authentication_params = _password_authentication(username, password)
                self.token, self.refresh_token, token_seconds = _get_tokens(authentication_params)
                self.token_expiration = time.time() + token_seconds
                break
            except Exception as e:
                if type(e) == requests.exceptions.HTTPError:
                    # handle invalid password
                    if e.response.status_code == 401:
                        print(f'Password or username invalid')
                        continue
                raise Exception('Failed to create TokenManager: ' + str(e))
        
    def _refresh_token(self):
        authentication_params = _refresh_authentication(self.refresh_token)
        try:
            self.token, self.refresh_token, token_seconds = _get_tokens(authentication_params)
            self.token_expiration = time.time() + token_seconds
        except Exception as e:
            raise Exception('Failed to refresh token: ' + str(e))

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

def _request_token(payload):
    headers = {
        'Authorization': f'Basic {_get_authorization()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # verify is false to disable the SSL cert verification
    return requests.post(Constants.TOKEN_URL, payload, headers=headers, verify=False)

def _get_tokens(authentication_params):
    r = _request_token(authentication_params)
    r.raise_for_status()
    j = r.json()
    access_token = j['access_token']
    refresh_token = j['refresh_token']
    expires_in_sec = j['expires_in']
    return access_token, refresh_token, expires_in_sec

def _get_userpass():
    username = os.environ['USER']
    password = None
    if username == Constants.DNASC_APP_USERNAME:
        try:
            yn = input(f'Run as {Constants.DNASC_APP_USERNAME}? (y/n): ')
        except KeyboardInterrupt:
            print()
            exit(1)
        if yn.lower() == 'y':
            try:
                _validate_credentials_file()
                return username, _read_password()
            except Exception as e:
                print(f'Failed to get {Constants.DNASC_APP_USERNAME} password: ' + str(e))
    password = _prompt_user_for_password(username)
    return username, password

def _validate_credentials_file():
    if os.path.isfile(Constants.CREDENTIALS_FILE_PATH):
        with open(Constants.CREDENTIALS_FILE_PATH) as f:
            j = json.load(f)
            if 'SMRT Link Password' in j:
                return True
            else:
                raise KeyError(f'{Constants.CREDENTIALS_FILE_PATH} missing key "SMRT Link Password".')
    else:
        raise Exception(f'{Constants.CREDENTIALS_FILE_PATH} does not exist.')

def _read_password():
    with open(Constants.CREDENTIALS_FILE_PATH) as f:
        j = json.load(f)
        return j['SMRT Link Password']

def _prompt_user_for_password(username):
    prompt = f'Enter the SMRT Link password for {username}, or exit and run as {Constants.DNASC_APP_USERNAME}: '
    try:
        password = getpass.getpass(prompt)
    except KeyboardInterrupt:
        print()
        exit(1)
    return password