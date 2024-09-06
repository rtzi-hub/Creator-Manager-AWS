pipeline {
    agent any

    parameters {
        choice(name: 'RESOURCE', choices: ['ec2', 's3', 'route53'], description: 'Choose AWS Resource')
        choice(name: 'ACTION', choices: ['create', 'list', 'start', 'stop'], description: 'Choose Action')
        string(name: 'INSTANCE_ID', defaultValue: '', description: 'Instance ID for EC2 actions')
        string(name: 'BUCKET_NAME', defaultValue: '', description: 'Bucket name for S3 actions')
        string(name: 'ZONE_NAME', defaultValue: '', description: 'Zone name for Route53 actions')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/rtzi-hub/Creator-Manager-AWS.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                source .venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Execute Action') {
            steps {
                script {
                    def command = ""
                    if (params.RESOURCE == 'ec2') {
                        if (params.ACTION == 'create') {
                            command = "python creator-ec2.py --action create --os ubuntu --type t3.nano"
                        } else if (params.ACTION == 'start' || params.ACTION == 'stop') {
                            if (params.INSTANCE_ID) {
                                command = "python creator-ec2.py --action ${params.ACTION} --instance-id ${params.INSTANCE_ID}"
                            } else {
                                error('Instance ID is required for start/stop actions.')
                            }
                        } else if (params.ACTION == 'list') {
                            command = "python creator-ec2.py --action list"
                        }
                    } else if (params.RESOURCE == 's3') {
                        if (params.ACTION == 'create') {
                            command = "python creator-s3.py --action create --bucket-name ${params.BUCKET_NAME} --public yes"
                        } else if (params.ACTION == 'list') {
                            command = "python creator-s3.py --action list"
                        }
                    } else if (params.RESOURCE == 'route53') {
                        if (params.ACTION == 'create') {
                            command = "python creator-route53.py --action create --zone-name ${params.ZONE_NAME}"
                        } else if (params.ACTION == 'list') {
                            command = "python creator-route53.py --action list"
                        }
                    }
                    
                    sh command
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
