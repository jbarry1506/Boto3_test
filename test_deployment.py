from client_locator import EC2Client
from ec2.vpc import VPC
from ec2.ec2 import EC2
from pprint import pprint
import vars

# TODO
# Define tests for all this code

def main():
    # Create a VPC -----------------------------------------------------------------
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()

    pprint('VPC created: ' + str(vpc_response))

    # Add name tag to VPC
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vars.vpc_name)

    print('Added name ' + vars.vpc_name + ' to ' + vpc_id)
# ok

    # Create an IGW
    igw_response = vpc.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    # Attach IGW to VPC
    print("Attaching IGW " + igw_id + ' to VPC ' + vpc_id)
    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # Create a Public Subnet -----------------------------------------------------------------
    # Error - public_cidr_block_ip is not defined
    public_subnet_response = vpc.create_subnet(vpc_id, vars.public_cidr_block_ip) 

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    print('Subnet created for VPC ' + ' : ' + str(public_subnet_response))

    # Add name tag to public subnet
    vpc.add_name_tag(public_subnet_id, vars.public_subnet_name) 

    # Create a public route table -----------------------------------------------------------------
    public_route_table_response = vpc.create_public_route_table(vpc_id)

    rtb_id = public_route_table_response['RouteTable']['RouteTableId']

    # Adding the igw to public route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associating igw with public route table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # Allow auto-assign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)

    # Create a Private Subnet -----------------------------------------------------------------
    private_subnet_response = vpc.create_subnet(vpc_id, vars.private_cidr_block_ip) 
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    print('Created private subnet ' + private_subnet_id + ' for VPC ' + vpc_id)

    # Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, vars.private_subnet_name) 

##################################################################################

    # EC2 Instances
    ec2 = EC2(ec2_client)

    # Create a key pair
    key_pair_response = ec2.create_key_pair(vars.key_pair_name)

    print('Created Key Pair with name ' + vars.key_pair_name + ':' + str(key_pair_response))

    # Create a Security Group
    public_security_group_description = 'Public Security Group for Public Subnet Internet Access'
    public_security_group_response = ec2.create_security_group(
        vars.public_security_group_name, public_security_group_description, vpc_id
    )

    public_security_group_id = public_security_group_response['GroupId']

    # Add Public Access to Security Group
    ec2.add_inbound_rule_to_sg(public_security_group_id)

    print('Added public access rule to Security Group ' + vars.public_security_group_name)

    user_data = """#!/bin/bash
                yum update -y
                yum install httpd24 -y
                service httpd start
                chkconfig httpd on
                echo "<html><body><h1>Hello from <b>Boto3</b> using Python!</h1></body></html>" > /var/www/html/index.html
                """

    # Launch a public EC2 Instance
    ec2.launch_ec2_instance(vars.ami_id, vars.key_pair_name, 1, 1, public_security_group_id, public_subnet_id, user_data)

    print('Launching Public EC2 Instance using AMI ' + vars.ami_id)

    # Adding another Security Group for Private EC2 Instance
    private_security_group_description = 'Private Security Group for Private Subnet'
    private_security_group_response = ec2.create_security_group(vars.private_security_group_name,
                                                                private_security_group_description, vpc_id)

    private_security_group_id = private_security_group_response['GroupId']

    # Add rule to private security group
    ec2.add_inbound_rule_to_sg(private_security_group_id)

    # Launch a private EC2 Instance
    ec2.launch_ec2_instance(vars.ami_id, vars.key_pair_name, 1, 1, private_security_group_id, private_subnet_id, """""")

    print('-----------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    main()

