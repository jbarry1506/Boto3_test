import boto3
from pprint import pprint
import vars

def main():

    ec2 = boto3.resource('ec2')
    # vpc = ec2.Vpc('id')
    print(boto3.__version__)
    ec2client = ec2.meta.client
    vpc = ec2.Vpc('vpc-0e3d68270dcaaa7a2')
    pprint(vpc)

if __name__ == "__main__":
    main()
    