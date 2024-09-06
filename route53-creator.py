import boto3
import argparse
from botocore.exceptions import ClientError

# Used for Route53 Service
route53_client = boto3.client('route53')

# Identifier
created_by_tag = 'CLI_Created'


# Create a new zone
def create_zone(domain_name):
    try:
        # Create the hosted zone
        response = route53_client.create_hosted_zone(
            Name=domain_name,
            CallerReference=str(hash(domain_name)),
            HostedZoneConfig={
                'Comment': 'Hosted zone created by CLI',
                'PrivateZone': False
            }
        )
        zone_id = response['HostedZone']['Id']

        # Add a tag to identify the zone
        route53_client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=[{'Key': 'CreatedBy', 'Value': created_by_tag}]
        )

        print(f"Hosted zone {domain_name} created with ID: {zone_id}")

    except ClientError as error:
        print(f"Error creating zone: {error}")


# Actions to manage the zone
def manage_record(zone_id, action, record_name, record_type, record_value):
    try:
        if action not in ['create', 'update', 'delete']:
            print("Invalid action. Choose from 'create', 'update', 'delete'.")
            return

        if action == 'create':
            change_batch = {
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': record_value}]
                        }
                    }
                ]
            }
        elif action == 'update':
            change_batch = {
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': record_value}]
                        }
                    }
                ]
            }
        elif action == 'delete':
            change_batch = {
                'Changes': [
                    {
                        'Action': 'DELETE',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,
                            'TTL': 300,
                            'ResourceRecords': [{'Value': record_value}]
                        }
                    }
                ]
            }

        # Update the DNS records
        route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch=change_batch
        )

        print(f"Record {action}d: {record_name} ({record_type}) with value {record_value}")

    except ClientError as error:
        print(f"Error managing record: {error}")


# List all DNS zones
def list_zones():
    try:
        response = route53_client.list_hosted_zones()
        for zone in response['HostedZones']:
            zone_id = zone['Id'].split('/')[-1]
            try:
                tags = route53_client.list_tags_for_resource(
                    ResourceType='hostedzone',
                    ResourceId=zone_id
                )['ResourceTagSet']['Tags']

                if any(tag['Key'] == 'CreatedBy' and tag['Value'] == created_by_tag for tag in tags):
                    print(f"Zone ID: {zone_id}, Name: {zone['Name']}")
            except ClientError as error:
                print(f"Error retrieving tags for zone {zone['Name']}: {error}")
    except ClientError as error:
        print(f"Error listing zones: {error}")


# Active Commands
def main():
    parser = argparse.ArgumentParser(description='Manage Route53 DNS zones and records.')
    parser.add_argument('--action', choices=['create', 'update', 'delete', 'list'], required=True,
                        help='Action to perform: create, update, delete, or list')
    parser.add_argument('--domain', help='Domain name for creating a zone')
    parser.add_argument('--zone-id', help='ID of the hosted zone (required for record actions)')
    parser.add_argument('--record-name', help='Name of the DNS record')
    parser.add_argument('--record-type', choices=['A', 'CNAME', 'TXT'], help='Type of the DNS record')
    parser.add_argument('--record-value', help='Value of the DNS record')

    args = parser.parse_args()

    if args.action == 'create':
        if not args.domain:
            print("Domain name is required for creating a zone.")
        else:
            create_zone(args.domain)
    elif args.action in ['update', 'delete']:
        if not args.zone_id or not args.record_name or not args.record_type or not args.record_value:
            print("Zone ID, record name, type, and value are required for record actions.")
        else:
            manage_record(args.zone_id, args.action, args.record_name, args.record_type, args.record_value)
    elif args.action == 'list':
        list_zones()


if __name__ == "__main__":
    main()
