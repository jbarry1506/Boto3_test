import boto3
from pprint import pprint
import vars

def main():
    iam = boto3.client('iam')

    # create new iam user
    response = iam.delete_user(
        UserName = vars.new_iam_user
    )
    pprint(response)

    # list all iam users
    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        pprint(response)


if __name__ == "__main__":
    main()
    