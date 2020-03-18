import boto3
import json
from pprint import pprint
import vars

# create iam client
iam = boto3.client('iam')

# iam_managed_policy = {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "",
#             "Action": "",
#             "Resource": ""
#         },
#         {

#         }
#     ]
# }

all_local_policies = iam.list_policies(
    # 'All'|'AWS'|'Local'
    Scope= 'Local',
    # True|False
    OnlyAttached= False
    #PathPrefix='string',
    # 'PermissionsPolicy'|'PermissionsBoundary',
    #PolicyUsageFilter='PermissionsPolicy',
    #Marker='string',
    #MaxItems=123
)

# Need arn for policy
response = iam.get_policy(
    PolicyArn = all_local_policies['Policies'][0]['Arn']
    # PolicyArn = vars.policy_arn
)

pprint(response)