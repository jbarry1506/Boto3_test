import boto3
import json
from pprint import pprint
import vars

iam_client = boto3.resource('iam')
group = iam_client.Group(vars.iam_group)

response = group.add_user(
        UserName = vars.new_iam_user
    )

pprint(response)
