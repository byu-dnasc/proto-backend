import globus_sdk
import json

def _get_credentials():
    with open('credentials.json', 'r') as f:
        j = json.load(f)
    return j['Globus Client ID'], j['Globus Client Secret']

def get_authorizer():
    CLIENT_ID, CLIENT_SECRET = _get_credentials()
    ACL_CREATION_SCOPE="urn:globus:auth:scope:transfer.api.globus.org:all"

    return globus_sdk.ClientCredentialsAuthorizer(
        globus_sdk.ConfidentialAppAuthClient(
            CLIENT_ID,
            CLIENT_SECRET,
        ),
        ACL_CREATION_SCOPE
    )