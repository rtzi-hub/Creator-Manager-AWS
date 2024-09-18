# AWS Resource Management Scripts

This repository contains Python scripts for managing AWS resources using Boto3. The scripts provided here enable you to create, manage, and delete AWS EC2 instances, S3 buckets, and Route 53 DNS records. Follow the instructions below to activate and use each script.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Script Activation and Usage](#script-activation-and-usage)
   - [EC2 Creator](#1-ec2-creator-ec2-creatorpy)
   - [S3 Creator](#2-s3-creator-s3-creatorpy)
   - [Route 53 Creator](#3-route-53-creator-route53-creatorpy)
4. [Best Practices](#best-practices)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

## Prerequisites

1. **Python 3.6+**: Ensure Python 3.6 or higher is installed. Verify with:

   ```bash
   python --version
AWS Credentials: Configure your AWS credentials using AWS CLI:

aws configure
Alternatively, set the following environment variables:

export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
Installation
Clone the repository:

git clone https://github.com/yourusername/yourrepository.git
Navigate to the repository directory:

cd yourrepository
Install the required Python packages:

pip install -r requirements.txt
Script Activation and Usage
1. EC2 Creator (ec2-creator.py)
This script allows you to manage AWS EC2 instances. Follow these steps to activate and use the EC2 creator script.

Usage:

python ec2-creator.py [options]
Options:

--create: Create a new EC2 instance.
--terminate: Terminate an existing EC2 instance.
--list: List all EC2 instances.
Examples:

Create a new EC2 instance:

python ec2-creator.py --create --instance-type t2.micro --key-name my-key --ami-id ami-12345678
--instance-type: Type of EC2 instance (e.g., t2.micro).
--key-name: Name of the key pair for SSH access.
--ami-id: AMI ID to use for the instance.
Terminate an existing EC2 instance:

python ec2-creator.py --terminate --instance-id i-1234567890abcdef0
--instance-id: ID of the EC2 instance to terminate.
List all EC2 instances:

python ec2-creator.py --list
2. S3 Creator (s3-creator.py)
This script allows you to manage AWS S3 buckets and files. Follow these steps to activate and use the S3 creator script.

Usage:

python s3-creator.py [options]
Options:

--create-bucket: Create a new S3 bucket.
--upload-file: Upload a file to an S3 bucket.
--list-buckets: List all S3 buckets.
Examples:

Create a new S3 bucket:

python s3-creator.py --create-bucket --bucket-name my-bucket
--bucket-name: Name of the new S3 bucket.
Upload a file to an S3 bucket:

python s3-creator.py --upload-file --bucket-name my-bucket --file-path /path/to/file.txt
--file-path: Path to the file you want to upload.
List all S3 buckets:

python s3-creator.py --list-buckets
3. Route 53 Creator (route53-creator.py)
This script allows you to manage DNS records in Route 53. Follow these steps to activate and use the Route 53 creator script.

Usage:

python route53-creator.py [options]
Options:

--create-record: Create a new DNS record.
--delete-record: Delete an existing DNS record.
--list-records: List all DNS records.
Examples:

Create a new DNS record:

python route53-creator.py --create-record --zone-id Z1234567890 --record-name example.com --record-type A --record-value 192.0.2.1
--zone-id: ID of the Route 53 hosted zone.
--record-name: Name of the DNS record.
--record-type: Type of DNS record (e.g., A, CNAME).
--record-value: Value for the DNS record (e.g., IP address).
Delete an existing DNS record:

python route53-creator.py --delete-record --zone-id Z1234567890 --record-name example.com --record-type A
--zone-id: ID of the Route 53 hosted zone.
--record-name: Name of the DNS record to delete.
--record-type: Type of DNS record.
List all DNS records:

python route53-creator.py --list-records --zone-id Z1234567890
--zone-id: ID of the Route 53 hosted zone.
