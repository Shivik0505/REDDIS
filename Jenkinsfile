pipeline {
    agent any

    // SCM Polling - check for changes every 5 minutes
    triggers {
        pollSCM('H/5 * * * *')
    }

    parameters {
        booleanParam(name: 'autoApprove', defaultValue: true, description: 'Automatically run apply after generating plan?')
        choice(name: 'action', choices: ['apply', 'destroy'], description: 'Select the action to perform')
        string(name: 'keyPairName', defaultValue: 'redis-infra-key', description: 'AWS Key Pair name to use')
        booleanParam(name: 'recreateKeyPair', defaultValue: false, description: 'Force recreate key pair if it exists?')
        booleanParam(name: 'skipAnsible', defaultValue: false, description: 'Skip Ansible configuration step?')
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        KEY_PAIR_NAME = "${params.keyPairName}"
        TF_IN_AUTOMATION = 'true'
        TF_INPUT = 'false'
        ANSIBLE_HOST_KEY_CHECKING = 'False'
        ANSIBLE_CONFIG = './ansible.cfg'
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('SCM Checkout') {
            steps {
                echo "=== SCM Checkout ==="
                checkout scm
                script {
                    def commitId = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    def commitMsg = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    echo "✅ Commit: ${commitId}"
                    echo "📝 Message: ${commitMsg}"
                }
            }
        }

        stage('Environment Validation') {
            steps {
                echo "=== Environment Validation ==="
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        aws sts get-caller-identity
                        terraform version || echo "⚠️ Terraform not found"
                        ansible --version || echo "⚠️ Ansible not found"
                    '''
                }
            }
        }

        stage('Key Pair Management') {
            when { expression { return params.action == 'apply' } }
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        if aws ec2 describe-key-pairs --key-names "$KEY_PAIR_NAME" --region $AWS_DEFAULT_REGION >/dev/null 2>&1; then
                            echo "✅ Key pair exists"
                            if [ "${recreateKeyPair}" = "true" ]; then
                                aws ec2 delete-key-pair --key-name "$KEY_PAIR_NAME" --region $AWS_DEFAULT_REGION
                                aws ec2 create-key-pair --key-name "$KEY_PAIR_NAME" --region $AWS_DEFAULT_REGION --query 'KeyMaterial' --output text > "${KEY_PAIR_NAME}.pem"
                                chmod 400 "${KEY_PAIR_NAME}.pem"
                            fi
                        else
                            aws ec2 create-key-pair --key-name "$KEY_PAIR_NAME" --region $AWS_DEFAULT_REGION --query 'KeyMaterial' --output text > "${KEY_PAIR_NAME}.pem"
                            chmod 400 "${KEY_PAIR_NAME}.pem"
                        fi
                    '''
                }
            }
        }

        stage('Infrastructure') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    script {
                        dir('terraform') {
                            if (params.action == 'apply') {
                                sh '''
                                    terraform init -input=false
                                    terraform validate
                                    terraform plan -input=false -out=tfplan -var="key-name=${KEY_PAIR_NAME}"
                                    terraform apply -input=false tfplan
                                    terraform output -json > ../terraform-outputs.json
                                '''
                            } else {
                                sh '''
                                    terraform init -input=false
                                    terraform destroy -input=false -var="key-name=${KEY_PAIR_NAME}" --auto-approve
                                '''
                            }
                        }
                    }
                }
            }
        }

        stage('Wait for Infrastructure') {
            when {
                allOf {
                    expression { return params.autoApprove }
                    expression { return params.action == 'apply' }
                }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        echo "⏳ Waiting for instances..."
                        sleep 90
                        aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=redis-*" --query 'Reservations[].Instances[].{Name:Tags[?Key==`Name`].Value|[0],State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress}' --output table --region $AWS_DEFAULT_REGION
                    '''
                }
            }
        }

        stage('Ansible Configuration') {
            when {
                allOf {
                    expression { return params.autoApprove }
                    expression { return params.action == 'apply' }
                    expression { return !params.skipAnsible }
                }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        # Create inventory
                        ./create-clean-inventory.sh
                        
                        # Test connectivity
                        ansible all -i inventory.ini -m ping --timeout=30 || echo "⚠️ Connectivity issues"
                        
                        # Run playbook
                        ansible-playbook -i inventory.ini playbook.yml --timeout=120 -v || echo "⚠️ Ansible issues - manual config may be needed"
                    '''
                }
            }
        }

        stage('Generate Connection Guide') {
            when {
                allOf {
                    expression { return params.autoApprove }
                    expression { return params.action == 'apply' }
                }
            }
            steps {
                sh '''
                    PUBLIC_IP=$(aws ec2 describe-instances --region $AWS_DEFAULT_REGION --filters "Name=tag:Name,Values=redis-public" "Name=instance-state-name,Values=running" --query 'Reservations[].Instances[].PublicIpAddress' --output text)
                    PRIVATE_IPS=($(aws ec2 describe-instances --region $AWS_DEFAULT_REGION --filters "Name=tag:Name,Values=redis-private*" "Name=instance-state-name,Values=running" --query 'Reservations[].Instances[].PrivateIpAddress' --output text))
                    
                    cat > connection-guide.txt << EOF
Redis Infrastructure Connection Guide
====================================
Bastion Host: ${PUBLIC_IP}
Redis Nodes: ${PRIVATE_IPS[@]}

Connect to Bastion:
ssh -i ${KEY_PAIR_NAME}.pem ubuntu@${PUBLIC_IP}

Connect to Redis Nodes:
ssh -i ${KEY_PAIR_NAME}.pem -J ubuntu@${PUBLIC_IP} ubuntu@${PRIVATE_IPS[0]}
ssh -i ${KEY_PAIR_NAME}.pem -J ubuntu@${PUBLIC_IP} ubuntu@${PRIVATE_IPS[1]}
ssh -i ${KEY_PAIR_NAME}.pem -J ubuntu@${PUBLIC_IP} ubuntu@${PRIVATE_IPS[2]}
EOF
                '''
            }
        }
    }

    post {
        always {
            script {
                if (fileExists("${params.keyPairName}.pem")) {
                    archiveArtifacts artifacts: "${params.keyPairName}.pem", allowEmptyArchive: true
                }
                if (fileExists('terraform-outputs.json')) {
                    archiveArtifacts artifacts: 'terraform-outputs.json', allowEmptyArchive: true
                }
                if (fileExists('connection-guide.txt')) {
                    archiveArtifacts artifacts: 'connection-guide.txt', allowEmptyArchive: true
                }
            }
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed - check logs for details'
        }
    }
}
