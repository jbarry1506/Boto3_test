import boto3
from pprint import pprint
import vars

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
response = ec2_client.describe_vpcs()
# pprint(response)

"""
To delete a VPC, it is necessary to handle the following preliminary items
    # Terminate all instances
    # Delete all subnets
    # Delete custom security groups 
    # and custom route tables
    # Detach any internet gateways 
    # or virtual private gateways

This code should get any necessary information for that purpose
"""

# TODO:
    # turn this into a function module
    # return variables, lists, or dicts to the vars file for use
    # build unit tests
    # get code review

for vpc in response['Vpcs']:
    print(vpc['VpcId'])
    if vpc['VpcId'] == vars.unknown_vpc_id:
        print('Found it!')
        vpc_del = ec2_resource.Vpc(vpc['VpcId'])

        # describe internet gateways
        print('\n------internet gateways------')
        for ig in vpc_del.internet_gateways.all():
            pprint(ig.id)
            ig_response = ec2_client.describe_internet_gateways(
                InternetGatewayIds=[
                    ig.id
                ]
            )
            pprint(ig_response)

        # describe instances
        print('\n------instances------')
        for inst in vpc_del.instances.all():
            # pprint(inst.id)
            inst_response = ec2_client.describe_instances(
                InstanceIds = [
                    inst.id
                ]
            )
            
            this_instance = inst_response['Reservations'][0]['Instances'][0]
            this_sg_gn = this_instance['SecurityGroups'][0]['GroupName']
            this_sg_gid = this_instance['SecurityGroups'][0]['GroupId']
            this_instance_state = this_instance['State']['Name']
            this_sub = this_instance['SubnetId']

            print("Instance State: {}".format(this_instance_state))
            print("Device Name: {}".format(this_instance['KeyName']))
            print("Instance Id: {}".format(this_instance['InstanceId']))
            print("Device Mappings:")
            # pprint(this_instance['BlockDeviceMappings'])
            for bdm in this_instance['BlockDeviceMappings']:
                print("\tEBS Volume Id: {}".format(bdm['Ebs']['VolumeId']))
                print("\tEBS Status: {}".format(bdm['Ebs']['Status']))
                print("\tEBS Delete on Termination: {}".format(bdm['Ebs']['DeleteOnTermination']))
            print("Device State: {}".format(this_instance['Monitoring']['State']))
            print("Image Id: {}".format(this_instance['ImageId']))
            print("Security Group Name: {}".format(this_sg_gn))
            print("Security Group Id: {}".format(this_sg_gid))
            print("Subnet: {}".format(this_sub))
            print("------------------------------------------------------------\n")
            

        # describe subnets
        print('\n------subnets------')
        for subnet in vpc_del.subnets.all():
            pprint(subnet.id)
            subnet_response = ec2_client.describe_subnets(
                SubnetIds=[
                    subnet.id
                ]
            )
            # pprint(subnet_response)
            this_subnet = subnet_response['Subnets'][0]
            print("Subnet Id: {}".format(this_subnet['SubnetId']))
            print("Subnet ARN: {}".format(this_subnet['SubnetArn']))
            print("CIDR Block: {}".format(this_subnet['CidrBlock']))
            print("State: {}".format(this_subnet['State']))
            print("-----------------------------------------------------------\n")

        # describe route tables
        print('\n------route tables------')
        for rt in vpc_del.route_tables.all():
            # pprint(rt.id)
            rt_response = ec2_client.describe_route_tables(
                RouteTableIds=[
                    rt.id
                ]
            )
            this_rt = rt_response['RouteTables'][0]
            # pprint(this_rt)
            print("Route Table Id: {}".format(this_rt['RouteTableId']))
            # this line threw an error.  out of range - catch that ish!
                # after catching the error, the state is 'blackhole'
                # research and handle
            try:
                print("Association State: {}".format(this_rt['Associations'][0]['AssociationState']['State']))
            except:
                print("The association state is probably not available.")
                
            try:
                print("Route Table Association Id: {}".format(this_rt['Associations'][0]['RouteTableAssociationId']))
            except:
                print("The Route Table Association Id isn't there.")

            # can i enumerate the keys in a for loop like this and feed a list 
            for route in this_rt['Routes']:
                print("Destination CIDR Block: {}".format(route['DestinationCidrBlock']))
                print("Gateway Id: {}".format(route['GatewayId']))
                print("State: {}".format(route['State']))
                print("************\n")
            print("-----------------------------------------------------------\n")

        # describe security groups
        print('\n------security groups------')
        for sg in vpc_del.security_groups.all():
            print("\n********* {} **********".format(sg.id))
            
            sg_response = ec2_client.describe_security_groups(
                GroupIds=[
                    sg.id
                ]
            )
            # pprint(sg_response['SecurityGroups'][0])
            sgr = sg_response['SecurityGroups'][0]
            print("Group Name: {}".format(sgr['GroupName']))
            print("Group Id: {}".format(sgr['GroupId']))
            print("Description: {}".format(sgr['Description']))
            for perm in sgr['IpPermissions']:
                print("\nIp Permissions:")
                pprint(sgr['IpPermissions'])
            print("CIDR Ip Ranges: {}".format(sgr['IpPermissionsEgress'][0]['IpRanges'][0]['CidrIp']))
            # The tags key doesn't appear to be reachable for some reason
            # print("Tags: {}".format(sgr['Tags']))

        # describe network acls
        print('\n------network acls------')
        for nacl in vpc_del.network_acls.all():
            pprint(nacl.id)
            nacl_response = ec2_client.describe_network_acls(
                NetworkAclIds=[
                    nacl.id
                ]
            )
            pprint(nacl_response)

        # # describe vpc peering connections
        # print('\n------vpc peering connections------')
        # peering_connections_response = ec2_client.describe_vpc_peering_connections()
        # for pc in peering_connections_response:
        #     pprint(pc)

        # # describe vpc endpoints
        # print('\n------vpc endpoints------')
        # endpoint_response = ec2_client.describe_vpc_endpoints()
        # for ep in endpoint_response:
        #     pprint(ep)

        # # describe nat gateways
        # print('\n------nat gateways------')
        # nat_gateways_response = ec2_client.describe_nat_gateways()
        # for ng in nat_gateways_response:
        #     pprint(ng)

        # # describe vpn connections
        # print('\n------vpn connections------')
        # vpn_connections_response = ec2_client.describe_vpn_connections()
        # for vc in vpn_connections_response:
        #     pprint(vc)

        # # describe vpn gateways
        # print('\n------vpn gateways------')
        # vpn_gateways_response = ec2_client.describe_vpn_gateways()
        # for vg in vpn_gateways_response:
        #     pprint(vg)

        # describe network interfaces
        print('\n------network interfaces------')
        for ni in vpc_del.network_interfaces.all():
            pprint(ni.id)
            ni_response = ec2_client.describe_network_interfaces(
                NetworkInterfaceIds=[
                    ni.id
                ]
            )
            pprint(ni_response)
