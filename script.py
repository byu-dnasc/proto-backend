#!/usr/bin/env python3

import globus_sdk
import requests

CLIENT_ID = "ee5204b1-b61f-45a1-8ea0-c1eea97125b6"
CLIENT_SECRET = ""
GUEST_COLLECTION_ID = "b550603b-7baa-43fa-b380-939d15549345" # DNASC
IDENTITY_ID = "19ff6717-c44d-4ab4-983c-1eb2095beba4" # aknaupp@byu.edu

ACL_CREATION_SCOPE="urn:globus:auth:scope:transfer.api.globus.org:all"

renewing_authorizer = globus_sdk.ClientCredentialsAuthorizer(
    globus_sdk.ConfidentialAppAuthClient(
        CLIENT_ID,
        CLIENT_SECRET,
    ),
    ACL_CREATION_SCOPE
)

# tc = globus_sdk.TransferClient(authorizer=renewing_authorizer)

# tc.endpoint_search(filter_scope="shared-by-me")
# tc.operation_ls('b550603b-7baa-43fa-b380-939d15549345', filter='name:~r64140*')

'''
rule_data = {
    "DATA_TYPE": "access",
    "principal_type": "identity",
    "principal": IDENTITY_ID,
    "path": "/ABHelix EXP23000689 CCS/",
    "permissions": "r",
}
transfer_client.add_endpoint_acl_rule(GUEST_COLLECTION_ID, rule_data)
'''
