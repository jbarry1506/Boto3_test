import boto3
import json
from pprint import pprint
import vars

iam_client = boto3.client('iam')

response = iam_client.create_login_profile(
    UserName = vars.new_iam_user,
    Password = vars.default_password,
    PasswordResetRequired = True
)

pprint(response)
