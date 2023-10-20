import globus_sdk
from globus.const import Constants
import json
import os

def _valid_credentials_file_accessible():
    if os.path.isfile(Constants.CREDENTIALS_FILE_PATH):
        with open(Constants.CREDENTIALS_FILE_PATH) as f:
            j = json.load(f)
            if 'Globus Client ID' in j and \
               'Globus Client Secret' in j:
                return True
            else:
                raise KeyError(f'{Constants.CREDENTIALS_FILE_PATH} missing key.')
    else:
        raise Exception(f'{Constants.CREDENTIALS_FILE_PATH} does not exist.')

def _read_id_secret():
    try:
        _valid_credentials_file_accessible()
    except Exception as e:
        print('Failed to access Globus index: ' + str(e))
    with open(Constants.CREDENTIALS_FILE_PATH) as f:
        j = json.load(f)
        return j['Globus Client ID'], j['Globus Client Secret']

def get_authorizer(scope):
    client_id, client_secret = _read_id_secret()
    return globus_sdk.ClientCredentialsAuthorizer(
        globus_sdk.ConfidentialAppAuthClient(
            client_id,
            client_secret
        ),
        scope
    )