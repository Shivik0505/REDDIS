#!/usr/bin/env python3
"""
Redis Infrastructure Diagram Generator using Python Diagrams
Creates a professional AWS infrastructure diagram for the Redis project
Based on the current deployed infrastructure
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC, PublicSubnet, PrivateSubnet, InternetGateway, NATGateway
from diagrams.aws.security import IAM
from diagrams.aws.general import User, InternetAlt1
from diagrams.aws.database import ElasticacheForRedis
from diagrams.onprem.client import Users
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.programming.language import Python
from diagrams.aws.management import Cloudformation

def create_redis_infrastructure_diagram():
    """Create the main Redis infrastructure diagram"""
    
    with Diagram("Redis Infrastructure on AWS - Multi-AZ Deployment", 
                 filename="redis_infrastructure_diagram", 
                 show=False, 
                 direction="TB",
                 graph_attr={
                     "fontsize": "20",
                     "bgcolor": "white",
                     "pad": "1.0",
                     "splines": "ortho"
                 }):
        
        # External users and internet
        users = Users("DevOps Team")
        internet = InternetAlt1("Internet")
        
        with Cluster("AWS Cloud (ap-south-1)"):
            
            with Cluster("Custom VPC (10.0.0.0/16)\nvpc-0bb85e2fb441d0fdd"):
                
                # Internet Gateway
                igw = InternetGateway("Internet Gateway")
                
                with Cluster("Public Subnet (10.0.1.0/24)\nap-south-1b"):
                    # Bastion Host
                    bastion = EC2("Bastion Host\ni-0a5f4742d750b6f1d\n3.110.104.52")
                    
                    # NAT Gateway
                    nat = NATGateway("NAT Gateway\nElastic IP")
                
                # Security Groups
                with Cluster("Security Groups"):
                    public_sg = IAM("Public SG\nSSH(22), HTTP(80)\nICMP")
                    private_sg = IAM("Private SG\nSSH(22), Redis(6379)\nCluster(16379-16384)")
                
                # Private Subnets with Redis Nodes
                with Cluster("Private Subnet 1 (10.0.2.0/24)\nap-south-1a"):
                    redis1 = EC2("Redis Node 1\ni-026ca7ca8e8fc9b10\n10.0.2.143")
                
                with Cluster("Private Subnet 2 (10.0.3.0/24)\nap-south-1b"):
                    redis2 = EC2("Redis Node 2\ni-02c2701141b0bdfb5\n10.0.3.32")
                
                with Cluster("Private Subnet 3 (10.0.4.0/24)\nap-south-1c"):
                    redis3 = EC2("Redis Node 3\ni-0e6b028479cc401bb\n10.0.4.214")
        
        # Connections
        users >> Edge(label="SSH Access") >> internet
        internet >> Edge(label="HTTPS/SSH") >> igw
        igw >> Edge(label="Public Access") >> bastion
        
        # Bastion to Redis nodes (SSH tunneling)
        bastion >> Edge(label="SSH Tunnel", style="dashed", color="red") >> redis1
        bastion >> Edge(label="SSH Tunnel", style="dashed", color="red") >> redis2
        bastion >> Edge(label="SSH Tunnel", style="dashed", color="red") >> redis3
        
        # NAT Gateway for outbound internet access
        nat >> Edge(label="Outbound Internet") >> igw
        redis1 >> Edge(label="Updates/Packages", style="dotted") >> nat
        redis2 >> Edge(label="Updates/Packages", style="dotted") >> nat
        redis3 >> Edge(label="Updates/Packages", style="dotted") >> nat
        
        # Redis cluster communication
        redis1 >> Edge(label="Cluster Sync", color="purple") >> redis2
        redis2 >> Edge(label="Cluster Sync", color="purple") >> redis3
        redis3 >> Edge(label="Cluster Sync", color="purple") >> redis1
        
        # Security group associations
        public_sg >> Edge(style="dotted", color="green") >> bastion
        private_sg >> Edge(style="dotted", color="blue") >> [redis1, redis2, redis3]

def create_jenkins_pipeline_diagram():
    """Create Jenkins CI/CD pipeline diagram"""
    
    with Diagram("Jenkins CI/CD Pipeline - Redis Infrastructure", 
                 filename="jenkins_pipeline_diagram", 
                 show=False, 
                 direction="LR",
                 graph_attr={
                     "fontsize": "18",
                     "bgcolor": "white",
                     "pad": "1.0"
                 }):
        
        # Source Control
        git_repo = Git("GitHub Repository\nSCM Polling (H/5 * * * *)")
        
        with Cluster("Jenkins Pipeline Stages"):
            jenkins = Jenkins("Jenkins Server")
            
            with Cluster("Pipeline Execution"):
                # Pipeline stages
                checkout = Python("1. SCM Checkout\nGit Clone")
                validate = Python("2. Environment Validation\nAWS CLI, Terraform, Ansible")
                keypair = Python("3. Key Pair Management\nAWS EC2 Key Pairs")
                terraform = Cloudformation("4. Infrastructure\nTerraform Apply")
                wait = Python("5. Wait for Infrastructure\nInstance Health Checks")
                ansible = Python("6. Ansible Configuration\nRedis Setup")
                guide = Python("7. Generate Connection Guide\nSSH Instructions")
        
        with Cluster("AWS Infrastructure"):
            vpc = VPC("VPC Creation")
            subnets = PublicSubnet("Subnets & Security Groups")
            instances = EC2("EC2 Instances\n1 Bastion + 3 Redis Nodes")
            redis_cluster = ElasticacheForRedis("Redis Cluster\nConfiguration")
        
        # Pipeline flow
        git_repo >> Edge(label="Webhook/Polling") >> jenkins
        jenkins >> checkout >> validate >> keypair >> terraform >> wait >> ansible >> guide
        
        # Infrastructure deployment
        terraform >> Edge(label="Provisions") >> vpc
        terraform >> Edge(label="Creates") >> subnets
        terraform >> Edge(label="Launches") >> instances
        ansible >> Edge(label="Configures") >> redis_cluster

def create_network_architecture_diagram():
    """Create detailed network architecture diagram"""
    
    with Diagram("Network Architecture - Redis Infrastructure", 
                 filename="network_architecture_diagram", 
                 show=False, 
                 direction="TB",
                 graph_attr={
                     "fontsize": "18",
                     "bgcolor": "white",
                     "pad": "1.0"
                 }):
        
        users = Users("Administrators")
        
        with Cluster("AWS Region: ap-south-1"):
            
            with Cluster("Availability Zones"):
                
                with Cluster("AZ-1a (ap-south-1a)"):
                    with Cluster("Private Subnet\n10.0.2.0/24"):
                        redis_1a = EC2("Redis Node 1\nPort: 6379\nCluster: 16379-16384")
                
                with Cluster("AZ-1b (ap-south-1b)"):
                    with Cluster("Public Subnet\n10.0.1.0/24"):
                        bastion_1b = EC2("Bastion Host\nSSH Gateway")
                        nat_1b = NATGateway("NAT Gateway")
                    
                    with Cluster("Private Subnet\n10.0.3.0/24"):
                        redis_1b = EC2("Redis Node 2\nPort: 6379\nCluster: 16379-16384")
                
                with Cluster("AZ-1c (ap-south-1c)"):
                    with Cluster("Private Subnet\n10.0.4.0/24"):
                        redis_1c = EC2("Redis Node 3\nPort: 6379\nCluster: 16379-16384")
            
            # Internet Gateway
            igw = InternetGateway("Internet Gateway")
        
        # Network connections
        users >> Edge(label="SSH (Port 22)") >> igw
        igw >> bastion_1b
        
        # Bastion to Redis nodes
        bastion_1b >> Edge(label="SSH Jump", style="dashed") >> redis_1a
        bastion_1b >> Edge(label="SSH Jump", style="dashed") >> redis_1b
        bastion_1b >> Edge(label="SSH Jump", style="dashed") >> redis_1c
        
        # Redis cluster communication
        redis_1a >> Edge(label="Redis Cluster", color="red") >> redis_1b
        redis_1b >> Edge(label="Redis Cluster", color="red") >> redis_1c
        redis_1c >> Edge(label="Redis Cluster", color="red") >> redis_1a
        
        # NAT Gateway for outbound
        [redis_1a, redis_1b, redis_1c] >> Edge(label="Outbound", style="dotted") >> nat_1b >> igw

if __name__ == "__main__":
    print("🎨 Creating Redis Infrastructure Diagrams...")
    print("=" * 50)
    
    # Create main infrastructure diagram
    print("📊 1. Creating main infrastructure diagram...")
    create_redis_infrastructure_diagram()
    print("   ✅ redis_infrastructure_diagram.png created")
    
    # Create Jenkins pipeline diagram
    print("🔄 2. Creating Jenkins pipeline diagram...")
    create_jenkins_pipeline_diagram()
    print("   ✅ jenkins_pipeline_diagram.png created")
    
    # Create network architecture diagram
    print("🌐 3. Creating network architecture diagram...")
    create_network_architecture_diagram()
    print("   ✅ network_architecture_diagram.png created")
    
    print("\n🎉 All diagrams created successfully!")
    print("\nGenerated files:")
    print("1. redis_infrastructure_diagram.png - Main AWS infrastructure")
    print("2. jenkins_pipeline_diagram.png - CI/CD pipeline flow")
    print("3. network_architecture_diagram.png - Detailed network topology")
    print("\n📋 Current Infrastructure Status:")
    print("• Bastion Host: 3.110.104.52 (i-0a5f4742d750b6f1d)")
    print("• Redis Node 1: 10.0.2.143 (i-026ca7ca8e8fc9b10)")
    print("• Redis Node 2: 10.0.3.32 (i-02c2701141b0bdfb5)")
    print("• Redis Node 3: 10.0.4.214 (i-0e6b028479cc401bb)")
    print("• VPC: vpc-0bb85e2fb441d0fdd (10.0.0.0/16)")
