import boto3
from pprint import pprint
import vars

client = boto3.client('ec2')

response = client.detach_internet_gateway(
    InternetGatewayId = vars.igw_id,
    VpcId = vars.unknown_vpc_id
)

pprint(response)