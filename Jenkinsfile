pipeline {
    agent any

    parameters {
        choice(name: 'RESOURCE', choices: ['ec2', 's3', 'route53'], description: 'Choose AWS Resource')
        choice(name: 'ACTION', choices: ['create', 'list', 'start', 'stop'], description: 'Choose Action')
        string(name: 'INSTANCE_ID', defaultValue: '', description: 'Instance ID for EC2 actions')
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'Bucket name for S3 actions')
        string(name: 'ZONE_NAME', defaultValue: '', description: 'Zone name for Route53 actions')
        choice(name: 'OS', choices: ['ubuntu', 'amazon'], description: 'Operating System for EC2 creation')
        choice(name: 'TYPE', choices: ['t3.nano', 't4g.nano'], description: 'Instance Type for EC2 creation')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/rtzi-hub/Creator-Manager-AWS.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    powershell '''
                    # Check if Python is installed
                    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
                        Write-Host "Python is not installed. Please install Python."
                        exit 1
                    }

                    # Create virtual environment if it doesn't exist
                    if (-not (Test-Path ".venv")) {
                        python -m venv .venv
                    }

                    # Activate virtual environment and install dependencies
                    .\\.venv\\Scripts\\Activate.ps1
                    if (Test-Path "requirements.txt") {
                        pip install -r requirements.txt
                    } else {
                        Write-Host "No requirements.txt file found!"
                        exit 1
                    }
                    '''
                }
            }
        }

        stage('Execute Action') {
            steps {
                script {
                    def command = ""

                    if (params.RESOURCE == 'ec2') {
                        if (params.ACTION == 'create') {
                            command = "python ec2-creator.py --action create --os ${params.OS} --type ${params.TYPE}"
                        } else if (params.ACTION == 'start' || params.ACTION == 'stop') {
                            if (params.INSTANCE_ID) {
                                command = "python ec2-creator.py --action ${params.ACTION} --instance-id ${params.INSTANCE_ID}"
                            } else {
                                error('Instance ID is required for start/stop actions.')
                            }
                        } else if (params.ACTION == 'list') {
                            command = "python ec2-creator.py --action list"
                        }
                    } else if (params.RESOURCE == 's3') {
                        if (params.ACTION == 'create') {
                            command = "python s3-creator.py --action create --bucket-name ${params.BUCKET_NAME} --public yes"
                        } else if (params.ACTION == 'list') {
                            command = "python s3-creator.py --action list"
                        }
                    } else if (params.RESOURCE == 'route53') {
                        if (params.ACTION == 'create') {
                            command = "python route53-creator.py --action create --zone-name ${params.ZONE_NAME}"
                        } else if (params.ACTION == 'list') {
                            command = "python route53-creator.py --action list"
                        }
                    }

                    if (command != "") {
                        powershell command
                    } else {
                        error('Invalid combination of parameters.')
                    }
                }
            }
        }

        stage('Finish') {
            steps {
                echo 'Operation completed.'
            }
        }
    }
}
