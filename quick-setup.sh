#!/bin/bash

# Quick Setup Script for Redis Infrastructure Template
# This script helps you get started quickly

echo "🚀 Redis Infrastructure Template - Quick Setup"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}📋 Prerequisites Check${NC}"
echo "======================"

# Check AWS CLI
if command -v aws &> /dev/null; then
    echo -e "${GREEN}✅ AWS CLI is installed${NC}"
    aws --version
else
    echo "❌ AWS CLI not found. Please install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check Terraform
if command -v terraform &> /dev/null; then
    echo -e "${GREEN}✅ Terraform is installed${NC}"
    terraform version
else
    echo "❌ Terraform not found. Please install: https://learn.hashicorp.com/tutorials/terraform/install-cli"
    exit 1
fi

# Check Ansible
if command -v ansible &> /dev/null; then
    echo -e "${GREEN}✅ Ansible is installed${NC}"
    ansible --version
else
    echo "❌ Ansible not found. Please install: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html"
    exit 1
fi

echo -e "\n${BLUE}🔧 Configuration${NC}"
echo "================"

# Check AWS credentials
if aws sts get-caller-identity &> /dev/null; then
    echo -e "${GREEN}✅ AWS credentials are configured${NC}"
    aws sts get-caller-identity
else
    echo -e "${YELLOW}⚠️ AWS credentials not configured. Run: aws configure${NC}"
fi

echo -e "\n${BLUE}📁 Project Structure${NC}"
echo "==================="
echo "Current directory: $(pwd)"
echo "Files in this template:"
ls -la

echo -e "\n${BLUE}🎯 Next Steps${NC}"
echo "============="
echo "1. Configure Jenkins:"
echo "   - Create new Pipeline job"
echo "   - Set SCM to point to this repository"
echo "   - Add AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)"
echo ""
echo "2. Enable SCM Polling:"
echo "   - Pipeline will check for changes every 5 minutes"
echo "   - Or set up GitHub webhook for instant triggering"
echo ""
echo "3. Test locally (optional):"
echo "   - cd terraform && terraform init && terraform plan"
echo "   - ansible --version"
echo ""
echo "4. Push to Git repository and let Jenkins handle the deployment!"

echo -e "\n${GREEN}✅ Setup complete! Your Redis infrastructure template is ready.${NC}"
