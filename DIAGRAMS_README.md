# Redis Infrastructure Diagrams

This directory contains professional infrastructure diagrams created using Python Diagrams library, representing the current deployed Redis infrastructure on AWS.

## 📊 Generated Diagrams

### 1. **redis_infrastructure_diagram.png**
- **Main AWS Infrastructure Diagram**
- Shows the complete multi-AZ Redis deployment
- Includes VPC, subnets, security groups, and EC2 instances
- Displays current IP addresses and instance IDs
- Network flow and security group associations

### 2. **jenkins_pipeline_diagram.png**
- **CI/CD Pipeline Flow**
- Jenkins Blue Ocean pipeline stages
- Infrastructure deployment process
- Terraform and Ansible integration
- Automated deployment workflow

### 3. **network_architecture_diagram.png**
- **Detailed Network Topology**
- Multi-AZ deployment across ap-south-1a/b/c
- Network segmentation and routing
- Redis cluster communication paths
- Security boundaries and access patterns

## 🏗️ Current Infrastructure Details

### **Deployed Resources**
```
VPC: vpc-0bb85e2fb441d0fdd (10.0.0.0/16)

Bastion Host:
- Instance: i-0a5f4742d750b6f1d
- Public IP: 3.110.104.52
- Private IP: 10.0.1.68
- Subnet: 10.0.1.0/24 (ap-south-1b)

Redis Nodes:
1. Node 1: i-026ca7ca8e8fc9b10 (10.0.2.143) - ap-south-1a
2. Node 2: i-02c2701141b0bdfb5 (10.0.3.32)  - ap-south-1b
3. Node 3: i-0e6b028479cc401bb (10.0.4.214) - ap-south-1c
```

### **Network Configuration**
- **Public Subnet**: 10.0.1.0/24 (Bastion + NAT Gateway)
- **Private Subnets**: 
  - 10.0.2.0/24 (ap-south-1a) - Redis Node 1
  - 10.0.3.0/24 (ap-south-1b) - Redis Node 2
  - 10.0.4.0/24 (ap-south-1c) - Redis Node 3

### **Security Groups**
- **Public SG**: SSH (22), HTTP (80), ICMP
- **Private SG**: SSH (22), Redis (6379), Cluster (16379-16384), ICMP

## 🛠️ Diagram Generation

### **Prerequisites**
```bash
# Create virtual environment
python3 -m venv diagram_env
source diagram_env/bin/activate

# Install dependencies
pip install diagrams
```

### **Generate Diagrams**
```bash
# Run the diagram generator
python create_redis_infrastructure_diagram.py
```

### **View Diagrams**
```bash
# Display all diagrams (optional)
python view_diagrams.py
```

## 📋 Diagram Features

### **Visual Elements**
- ✅ AWS service icons and branding
- ✅ Network flow arrows and connections
- ✅ Security group associations
- ✅ Multi-AZ deployment visualization
- ✅ Current IP addresses and instance IDs
- ✅ Professional layout and styling

### **Technical Accuracy**
- ✅ Matches current deployed infrastructure
- ✅ Correct network topology
- ✅ Accurate security group configurations
- ✅ Real instance IDs and IP addresses
- ✅ Proper AWS service representations

## 🔄 Jenkins Pipeline Visualization

The Jenkins pipeline diagram shows:
1. **SCM Checkout** - Git repository polling
2. **Environment Validation** - Tool verification
3. **Key Pair Management** - AWS EC2 key pairs
4. **Infrastructure** - Terraform deployment
5. **Wait for Infrastructure** - Health checks
6. **Ansible Configuration** - Redis setup
7. **Generate Connection Guide** - Access instructions

## 🌐 Network Architecture Details

The network diagram illustrates:
- **Multi-AZ deployment** across 3 availability zones
- **Bastion host** for secure SSH access
- **NAT Gateway** for outbound internet access
- **Redis cluster** communication between nodes
- **Security boundaries** and access controls

## 📞 Access Instructions

```bash
# Connect to bastion host
ssh -i redis-infra-key.pem ubuntu@3.110.104.52

# Connect to Redis nodes via bastion (jump server)
ssh -i redis-infra-key.pem -J ubuntu@3.110.104.52 ubuntu@10.0.2.143
ssh -i redis-infra-key.pem -J ubuntu@3.110.104.52 ubuntu@10.0.3.32
ssh -i redis-infra-key.pem -J ubuntu@3.110.104.52 ubuntu@10.0.4.214
```

## 🔧 Customization

To update diagrams with new infrastructure:
1. Modify `create_redis_infrastructure_diagram.py`
2. Update IP addresses and instance IDs
3. Regenerate diagrams
4. Commit changes to repository

## 📈 Benefits

- **Documentation**: Visual infrastructure documentation
- **Onboarding**: Easy understanding for new team members
- **Troubleshooting**: Clear network topology for debugging
- **Compliance**: Architecture documentation for audits
- **Planning**: Visual aid for infrastructure changes

---

**Generated on**: 2025-06-27  
**Infrastructure Status**: ✅ Deployed and Operational  
**Diagram Tool**: Python Diagrams Library  
**AWS Region**: ap-south-1 (Mumbai)
