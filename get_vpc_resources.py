import boto3
from pprint import pprint
import vars

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
response = ec2_client.describe_vpcs()
# pprint(response)

for vpc in response['Vpcs']:
    print(vpc['VpcId'])
    if vpc['VpcId'] == vars.vpc_id:
        print('Found it!')
        vpc_del = ec2_resource.Vpc(vpc['VpcId'])
        # describe internet gateways
        print('------internet gateways------\n')
        for ig in vpc_del.internet_gateways.all():
            pprint(ig)

        # describe subnets
        print('------subnets------\n')
        for subnet in vpc_del.subnets.all():
            pprint(subnet)

        # describe route tables
        print('------route tables------\n')
        for rt in vpc_del.route_tables.all():
            pprint(rt)

        # describe network acls
        print('------network acls------\n')
        for nacl in vpc_del.network_acls.all():
            pprint(nacl)

        # describe vpc peering connections
        print('------vpc peering connections------\n')
        peering_connections_response = ec2_client.describe_vpc_peering_connections()
        for pc in peering_connections_response:
            pprint(pc)

        # describe vpc endpoints
        print('------vpc endpoints------\n')
        endpoint_response = ec2_client.describe_vpc_endpoints()
        for ep in endpoint_response:
            pprint(ep)

        # describe nat gateways
        print('------nat gateways------\n')
        nat_gateways_response = ec2_client.describe_nat_gateways()
        for ng in nat_gateways_response:
            pprint(ng)

        # describe security groups
        print('------security groups------\n')
        for sg in vpc_del.security_groups.all():
            pprint(sg)

        # describe instances
        print('------instances------\n')
        for inst in vpc_del.instances.all():
            pprint(inst)

        # describe vpn connections
        print('------vpn connections------\n')
        vpn_connections_response = ec2_client.describe_vpn_connections()
        for vc in vpn_connections_response:
            pprint(vc)

        # describe vpn gateways
        print('------vpn gateways------\n')
        vpn_gateways_response = ec2_client.describe_vpn_gateways()
        for vg in vpn_gateways_response:
            pprint(vg)

        # describe network interfaces
        print('------network interfaces------\n')
        for ni in vpc_del.network_interfaces.all():
            pprint(ni)
