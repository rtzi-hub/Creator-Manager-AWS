import boto3
import argparse
from botocore.exceptions import ClientError

# Used for ec2 resource
ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

# Identifier
created_by_tag = 'CLI_Created'


# Launch a new EC2 instance < 2
def launch_new_instance(vpc_id, subnet_id, security_group_id, operating_system, instance_type):
    if count_running_instances() >= 2:
        print("You already have 2 running instances. Cannot create more.")
        return

    ami_id = get_latest_ami(operating_system)
    if not ami_id:
        print(f"Could not find a suitable AMI for OS: {operating_system}.")
        return

    try:
        new_instance = ec2_resource.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet_id,
            SecurityGroupIds=[security_group_id],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'CreatedBy', 'Value': created_by_tag}]
                }
            ]
        )
        print(f"New EC2 instance created: {new_instance[0].id}")
    except ClientError as error:
        print(f"Error while creating EC2 instance: {error}")


# Get the latest operating system
def get_latest_ami(operating_system):
    if operating_system == 'ubuntu':
        ami_filter = [{'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*']}]
    elif operating_system == 'amazon':
        ami_filter = [{'Name': 'name', 'Values': ['amzn2-ami-hvm-2.0.*-x86_64-gp2']}]
    else:
        print(f"Invalid operating system specified: {operating_system}")
        return None

    try:
        available_images = ec2_client.describe_images(Filters=ami_filter, Owners=['amazon'])['Images']
        if not available_images:
            print(f"No AMIs found for OS: {operating_system}")
            return None
        latest_image = sorted(available_images, key=lambda img: img['CreationDate'], reverse=True)[0]
        return latest_image['ImageId']
    except ClientError as error:
        print(f"Error while fetching AMIs: {error}")
        return None


# How many instances are currently running
def count_running_instances():
    running_instances = ec2_resource.instances.filter(
        Filters=[
            {'Name': 'tag:CreatedBy', 'Values': [created_by_tag]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    return sum(1 for _ in running_instances)


# Start or stop the EC2 instance using the instance ID
def control_instance(instance_id, action='start'):
    try:
        instance = ec2_resource.Instance(instance_id)
        if action == 'start':
            if instance.state['Name'] == 'stopped':
                instance.start()
                print(f"Started instance: {instance_id}")
            else:
                print(f"Instance {instance_id} is running already.")
        elif action == 'stop':
            if instance.state['Name'] == 'running':
                instance.stop()
                print(f"Stopped instance: {instance_id}")
            else:
                print(f"Instance {instance_id} is not stopped already")
    except ClientError as error:
        print(f"Error instance {instance_id}: {error}")


# List all EC2 instances
def list_all_instances():
    instances = ec2_resource.instances.filter(
        Filters=[{'Name': 'tag:CreatedBy', 'Values': [created_by_tag]}]
    )
    for instance in instances:
        print(f"Instance ID: {instance.id}, State: {instance.state['Name']}")


# Different commands
def main():
    parser = argparse.ArgumentParser(description='Create, manage, and list EC2 instances.')
    parser.add_argument('--os', choices=['amazon', 'ubuntu'], default='ubuntu',
                        help='Choose the operating system (amazon or ubuntu)')
    parser.add_argument('--type', choices=['t3.nano', 't4g.nano'], default='t3.nano',
                        help='Choose the instance type (t3.nano or t4g.nano)')
    parser.add_argument('--action', choices=['create', 'list', 'start', 'stop'], required=True,
                        help='Action to perform: create, list, start, stop')
    parser.add_argument('--instance-id', help='Instance ID to start or stop (required for start/stop actions)')

    args = parser.parse_args()

    # Exist services
    if args.action == 'create':
        my_vpc_id = 'vpc-085589eeda0ae85d1' #Change it to exist VPC
        my_subnet_id = 'subnet-0599162f6cd1dbe02' #Change it to exist Public Subnet
        my_security_group_id = 'sg-0c509f02d2f013d78' #Change it to exist Security Group

        launch_new_instance(
            vpc_id=my_vpc_id,
            subnet_id=my_subnet_id,
            security_group_id=my_security_group_id,
            operating_system=args.os,
            instance_type=args.type
        )
    elif args.action == 'list':
        list_all_instances()
    elif args.action == 'start' or args.action == 'stop':
        if not args.instance_id:
            print("Instance ID is required for start/stop actions.")
        else:
            control_instance(instance_id=args.instance_id, action=args.action)


if __name__ == "__main__":
    main()
