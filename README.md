## AWS CLI Management Tool - README

This script provides a command-line interface (CLI) for managing various AWS services, including EC2 instances, S3 buckets, and Route53 DNS zones. It simplifies common tasks and helps you automate your AWS infrastructure management.

### Prerequisites

* An AWS account with proper permissions for the desired actions.
* Python 3.x installed on your system.
* Boto3 library installed: `pip install boto3`

**Note:** You'll need to configure your AWS credentials before using the script. You can do this by setting environment variables, creating a credentials file, or using a configuration profile. Refer to the Boto3 documentation for details:  [https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)

### Usage

This script utilizes the `argparse` library to accept different commands and arguments. Run the script with the `--help` flag to see all available options and their descriptions:

```
python aws_cli_tool.py --help
```

**Supported Services and Actions:**

* **EC2 Instances:**
    * `create`: Launch a new EC2 instance (requires instance type, VPC ID, subnet ID, and operating system)
    * `list`: List all running EC2 instances with their tags
    * `start`: Start a stopped EC2 instance (requires instance ID)
    * `stop`: Stop a running EC2 instance (requires instance ID)

* **S3 Buckets:**
    * `create`: Create a new S3 bucket (requires bucket name, optionally set public access)
    * `upload`: Upload a file to an existing S3 bucket (requires bucket name and file path)
    * `list`: List all S3 buckets created by this script

* **Route53 DNS Zones:**
    * `create`: Create a new hosted zone (requires domain name)
    * `update`: Update an existing DNS record (requires zone ID, record details)
    * `delete`: Delete an existing DNS record (requires zone ID, record details)
    * `list`: List all Route53 zones created by this script (shows zone ID and domain name)


### Example Usage

**Launch a new EC2 instance:**

```
python aws_cli_tool.py --action create --os ubuntu --type t3.nano \
--vpc-id vpc-085589eeda0ae85d1 --subnet-id subnet-0599162f6cd1dbe02
```

**Create a new S3 bucket with public access:**

```
python aws_cli_tool.py --action create --bucket-name my-public-bucket --public
```

**Upload a file to an existing S3 bucket:**

```
python aws_cli_tool.py --action upload --bucket-name my-bucket --file /path/to/file.txt
```

**List all Route53 zones created by this script:**

```
python aws_cli_tool.py --action list
```

**Update a DNS record (replace placeholders with actual values):**

```
python aws_cli_tool.py --action update --zone-id Z1234567890EXAMPLE --record-name www \
--record-type A --record-value 10.0.0.1
```


### Additional Notes

* This script uses a tag (`CreatedBy: CLI_Created`) to identify resources created by itself.
* Always double-check your input parameters before running any actions that modify your AWS resources.
* Consider implementing error handling in your own scripts based on your specific needs.


This is a basic overview of the script's functionality. Feel free to explore the source code for further details and customization options.
