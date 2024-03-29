class Constants:
    HOSTNAME = 'localhost'
    SERVER_EP = f'http://{HOSTNAME}:9091'
    SERVICES_EP_BASE = SERVER_EP + '/smrt-link'
    STATUS_URL = SERVER_EP + '/status'
    TOKEN_URL = f'https://{HOSTNAME}:8243/SMRTLink/1.0.0/token'
    scopes = ['welcome', 'run-design', 'run-qc', 'openid', 'analysis', 'sample-setup', 'data-management', 'userinfo']
    SCOPE = ' '.join({s for s in scopes})
    CREDENTIALS_FILE_PATH = '/home/dnascapp/backend/credentials.json'
    DNASC_APP_USERNAME = 'dnascapp'
    INSTRUMENTS = {
        'Revio': [
            '84100'
        ],
        'Sequel II': [
            'Sequel II SQ54336U',
            '64140'
        ]
    }