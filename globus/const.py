class Constants:
    CREDENTIALS_FILE_PATH = '/home/dnascapp/backend/credentials.json' 
    APP_CLIENT_UUID = 'ee5204b1-b61f-45a1-8ea0-c1eea97125b6'
    visible_to_identities = [APP_CLIENT_UUID]
    VISIBLE_TO_URNS = [f'urn:globus:auth:identity:{i}' for i in visible_to_identities]
