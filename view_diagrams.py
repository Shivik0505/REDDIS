#!/usr/bin/env python3
"""
Simple script to display the generated infrastructure diagrams
"""

import os
from PIL import Image
import matplotlib.pyplot as plt

def display_diagrams():
    """Display all generated diagrams"""
    
    diagram_files = [
        "redis_infrastructure_diagram.png",
        "jenkins_pipeline_diagram.png", 
        "network_architecture_diagram.png"
    ]
    
    titles = [
        "Redis Infrastructure on AWS - Multi-AZ Deployment",
        "Jenkins CI/CD Pipeline - Redis Infrastructure",
        "Network Architecture - Redis Infrastructure"
    ]
    
    fig, axes = plt.subplots(3, 1, figsize=(16, 24))
    fig.suptitle('Redis Infrastructure Diagrams', fontsize=20, fontweight='bold')
    
    for i, (filename, title) in enumerate(zip(diagram_files, titles)):
        if os.path.exists(filename):
            img = Image.open(filename)
            axes[i].imshow(img)
            axes[i].set_title(title, fontsize=14, fontweight='bold', pad=20)
            axes[i].axis('off')
        else:
            axes[i].text(0.5, 0.5, f'Diagram not found: {filename}', 
                        ha='center', va='center', fontsize=12)
            axes[i].set_title(title, fontsize=14, fontweight='bold')
            axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig('combined_diagrams.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("📊 All diagrams displayed!")
    print("💾 Combined diagram saved as 'combined_diagrams.png'")

if __name__ == "__main__":
    display_diagrams()
