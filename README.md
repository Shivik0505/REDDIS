# Redis Infrastructure Template

## 🎯 Overview
This is a streamlined Redis infrastructure template for AWS deployment using Jenkins SCM polling pipeline.

## 🏗️ Architecture
- **Custom VPC** (10.0.0.0/16) with multi-AZ deployment
- **1 Bastion Host** (public subnet)
- **3 Redis Nodes** (private subnets across 3 AZs)
- **Security Groups** with proper Redis port configurations
- **NAT Gateway** for private subnet internet access

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Jenkins with required plugins
- Terraform installed
- Ansible installed

### Jenkins Setup
1. Create new Pipeline job
2. Configure SCM: Point to your Git repository
3. Set up AWS credentials in Jenkins:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### Deployment
1. Push code to repository
2. Jenkins SCM polling will detect changes (every 5 minutes)
3. Pipeline will automatically deploy infrastructure
4. Download artifacts: SSH key, connection guide

## 📋 Pipeline Stages
1. **SCM Checkout** - Pull latest code
2. **Environment Validation** - Check AWS credentials and tools
3. **Key Pair Management** - Create/manage SSH keys
4. **Infrastructure** - Terraform provisioning
5. **Wait for Infrastructure** - Ensure instances are ready
6. **Ansible Configuration** - Configure Redis cluster
7. **Generate Connection Guide** - Create access instructions

## 🔧 Configuration Files
- `Jenkinsfile` - Jenkins pipeline definition
- `terraform/` - Infrastructure as Code
- `ansible.cfg` - Ansible configuration
- `playbook.yml` - Redis configuration playbook
- `create-clean-inventory.sh` - Dynamic inventory creation

## 📊 Infrastructure Details
- **Region**: ap-south-1 (Mumbai)
- **Instance Type**: t3.micro
- **Key Pair**: redis-infra-key
- **VPC CIDR**: 10.0.0.0/16

## 🔗 Connection
After deployment, use the generated connection guide to access your infrastructure:
```bash
# Connect to bastion
ssh -i redis-infra-key.pem ubuntu@<PUBLIC_IP>

# Connect to Redis nodes via bastion
ssh -i redis-infra-key.pem -J ubuntu@<BASTION_IP> ubuntu@<REDIS_NODE_IP>
```

## 🧹 Cleanup
Set pipeline parameter `action=destroy` to clean up all resources.

## 📞 Support
Check Jenkins console output for detailed logs and troubleshooting information.
