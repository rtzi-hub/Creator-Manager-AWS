import boto3
import argparse
from botocore.exceptions import ClientError

# Used for S3 resource
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

# Identifier
created_by_tag = 'CLI_Created'


# Launch a new S3 Storage
def create_bucket(bucket_name, public_access):
    try:
        s3_resource.create_bucket(Bucket=bucket_name)
        # Add a tag to identify the bucket
        s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={'TagSet': [{'Key': 'CreatedBy', 'Value': created_by_tag}]}
        )

        if public_access:
            confirm = input("Are you sure you want to make this bucket public? (yes/no): ")
            if confirm.lower() == 'yes':
                s3_client.put_bucket_acl(Bucket=bucket_name, ACL='public-read')
                print(f"Bucket {bucket_name} is created with public access.")
            else:
                print(f"Bucket {bucket_name} is created with private access.")
        else:
            print(f"Bucket {bucket_name} is created with private access.")

    except ClientError as error:
        print(f"Error creating bucket: {error}")


# Upload a file to S3 bucket
def upload_file(bucket_name, file_path):
    try:
        s3_client.upload_file(file_path, bucket_name, file_path)
        print(f"File {file_path} uploaded to bucket {bucket_name}.")
    except ClientError as error:
        print(f"Error uploading file: {error}")


# List all S3 buckets created by the CLI
def list_buckets():
    try:
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            try:
                # Attempt to get the tags for the bucket
                tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
                # Check if the bucket was created by the CLI
                if any(tag['Key'] == 'CreatedBy' and tag['Value'] == created_by_tag for tag in tags):
                    print(f"Bucket ID: {bucket['Name']}")
            except ClientError as error:
                if error.response['Error']['Code'] == 'NoSuchTagSet':
                    # If the bucket has no tags, skip it
                    continue
                else:
                    print(f"Error retrieving tags for bucket {bucket['Name']}: {error}")
    except ClientError as error:
        print(f"Error listing buckets: {error}")

# Active Commands
def main():
    parser = argparse.ArgumentParser(description='Manage S3 buckets.')
    parser.add_argument('--action', choices=['create', 'upload', 'list'], required=True,
                        help='Action to perform: create, upload, or list')
    parser.add_argument('--bucket-name', help='Name of the bucket (required for create/upload actions)')
    parser.add_argument('--public', action='store_true', help='Create bucket with public access (for create action)')
    parser.add_argument('--file', help='File path to upload (required for upload action)')

    args = parser.parse_args()

    if args.action == 'create':
        if not args.bucket_name:
            print("Bucket name is required for creating a bucket.")
        else:
            create_bucket(args.bucket_name, args.public)
    elif args.action == 'upload':
        if not args.bucket_name or not args.file:
            print("Bucket name and file path are required for uploading a file.")
        else:
            upload_file(args.bucket_name, args.file)
    elif args.action == 'list':
        list_buckets()


if __name__ == "__main__":
    main()
