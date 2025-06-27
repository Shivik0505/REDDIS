#!/bin/bash

# Cleanup script for duplicate Redis instances
set -e

echo "🧹 Redis Infrastructure Cleanup Script"
echo "======================================"

# Get all Redis instances
echo "🔍 Scanning for Redis instances..."
INSTANCES=$(aws ec2 describe-instances \
    --region ap-south-1 \
    --filters "Name=tag:Name,Values=redis-*" "Name=instance-state-name,Values=running,pending,stopping,stopped" \
    --query 'Reservations[].Instances[].{InstanceId:InstanceId,Name:Tags[?Key==`Name`].Value|[0],State:State.Name,LaunchTime:LaunchTime}' \
    --output json)

echo "📊 Found instances:"
echo "$INSTANCES" | jq -r '.[] | "\(.Name): \(.InstanceId) (\(.State)) - \(.LaunchTime)"'

# Count instances by name
PUBLIC_COUNT=$(echo "$INSTANCES" | jq -r '.[] | select(.Name=="redis-public") | .InstanceId' | wc -l)
PRIVATE1_COUNT=$(echo "$INSTANCES" | jq -r '.[] | select(.Name=="redis-private-1") | .InstanceId' | wc -l)
PRIVATE2_COUNT=$(echo "$INSTANCES" | jq -r '.[] | select(.Name=="redis-private-2") | .InstanceId' | wc -l)
PRIVATE3_COUNT=$(echo "$INSTANCES" | jq -r '.[] | select(.Name=="redis-private-3") | .InstanceId' | wc -l)

echo ""
echo "📈 Instance counts:"
echo "  redis-public: $PUBLIC_COUNT"
echo "  redis-private-1: $PRIVATE1_COUNT"
echo "  redis-private-2: $PRIVATE2_COUNT"
echo "  redis-private-3: $PRIVATE3_COUNT"

# Check for duplicates
TOTAL_EXPECTED=4
TOTAL_FOUND=$((PUBLIC_COUNT + PRIVATE1_COUNT + PRIVATE2_COUNT + PRIVATE3_COUNT))

if [ $TOTAL_FOUND -eq $TOTAL_EXPECTED ]; then
    echo "✅ Perfect! Found exactly $TOTAL_EXPECTED instances as expected."
    exit 0
elif [ $TOTAL_FOUND -lt $TOTAL_EXPECTED ]; then
    echo "⚠️  Warning: Found only $TOTAL_FOUND instances, expected $TOTAL_EXPECTED"
    echo "   Some instances might be missing or in different states"
    exit 1
else
    echo "❌ Found $TOTAL_FOUND instances, expected $TOTAL_EXPECTED"
    echo "   Duplicates detected!"
    
    read -p "🤔 Do you want to clean up duplicates? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🧹 Cleaning up duplicates..."
        
        # For each instance type, keep the newest and terminate the rest
        for INSTANCE_TYPE in "redis-public" "redis-private-1" "redis-private-2" "redis-private-3"; do
            DUPLICATE_IDS=$(echo "$INSTANCES" | jq -r ".[] | select(.Name==\"$INSTANCE_TYPE\") | .InstanceId" | head -n -1)
            
            if [ ! -z "$DUPLICATE_IDS" ]; then
                echo "🗑️  Terminating older $INSTANCE_TYPE instances..."
                for ID in $DUPLICATE_IDS; do
                    echo "   Terminating: $ID"
                    aws ec2 terminate-instances --region ap-south-1 --instance-ids $ID
                done
            fi
        done
        
        echo "✅ Cleanup completed!"
        echo "⏳ Wait a few minutes for instances to terminate, then run the script again to verify"
    else
        echo "❌ Cleanup cancelled. Manual intervention required."
        exit 1
    fi
fi
