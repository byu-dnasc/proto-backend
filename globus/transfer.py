import globus_sdk

GUEST_COLLECTION_ID = "b550603b-7baa-43fa-b380-939d15549345" # DNASC
IDENTITY_ID = "19ff6717-c44d-4ab4-983c-1eb2095beba4" # aknaupp@byu.edu

def get_transfer_client(authorizer):
    return globus_sdk.TransferClient(authorizer=authorizer)

def get_endpoints(transfer_client):
    return transfer_client.endpoint_search(filter_scope='shared-by-me')

def ls_filename_starts_with(transfer_client, txt):
    return transfer_client.operation_ls(GUEST_COLLECTION_ID, 
                                        path='/',
                                        filter=f'name:~{txt}*')

def add_acl_rule(transfer_client, rule_data):
    rule_data = {
        "DATA_TYPE": "access",
        "principal_type": "identity",
        "principal": IDENTITY_ID,
        "path": "/ABHelix EXP23000689 CCS/",
        "permissions": "r",
    }
    return transfer_client.add_endpoint_acl_rule(GUEST_COLLECTION_ID, rule_data)
