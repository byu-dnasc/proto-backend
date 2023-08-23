class Constants:
    HOSTNAME = 'localhost'
    SERVER_EP = f'http://{HOSTNAME}:9091'
    SERVICES_EP_BASE = SERVER_EP + '/smrt-link'
    STATUS_URL = SERVER_EP + '/status'
    TOKEN_URL = f'https://{HOSTNAME}:8243/SMRTLink/1.0.0/token'
