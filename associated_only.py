import boto3
import pandas as pd
from datetime import datetime, timedelta

def is_snapshot_old_enough(age_days):
    # Check if the age is greater than or equal to 1 day
    return age_days >= 105 #initally we can declare how much  ever we want , also days.

def is_snapshot_in_use(snapshot_id, region_name):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2', region_name=region_name)
    
    # Check if any instances are using the snapshot as their root or data volume
    instances = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for volume in instance.get('BlockDeviceMappings', []):
                if 'Ebs' in volume and 'SnapshotId' in volume['Ebs'] and volume['Ebs']['SnapshotId'] == snapshot_id:
                    return True
    
    # Check if the snapshot is used by any AMIs
    images = ec2_client.describe_images(
        Filters=[
            {'Name': 'block-device-mapping.snapshot-id', 'Values': [snapshot_id]}
        ]
    )
    for image in images['Images']:
        return True
    
    return False

def display_associated_snapshots_from_excel(excel_file_path):
    # Read Excel file using pandas
    snapshot_df = pd.read_excel(excel_file_path)
    
    # Iterate over rows in the dataframe
    for index, row in snapshot_df.iterrows():
        snapshot_id = row['Snapshot ID']
        region = row['Region']
        age_days = row['Age (Days)']
        
        # Map human-readable region names to AWS region identifiers
        region_mapping = {
            'EU (Ireland)': 'eu-west-1',
            'Asia Pacific (Singapore)': 'ap-southeast-1',
            'Asia Pacific (Mumbai)': 'ap-south-1',
            'US East (N. Virginia)': 'us-east-1',
            # Add more mappings as needed
        }
        region_name = region_mapping.get(region, region)  # Get AWS region identifier or use the same if not found
        
        # Check if the snapshot is older than or equal to 1 day and is in use
        if is_snapshot_old_enough(age_days) and is_snapshot_in_use(snapshot_id, region_name):
            print(f"Snapshot ID: {snapshot_id}")
            print(f"Region: {region}")
            print(f"Age (Days): {age_days}")
            print("Associated with a resource or service")
            print("--------------------------------------------------")

if __name__ == "__main__":
    excel_file_path = 'infra_clean_up.xlsx'  # Provide the path to your Excel file
    display_associated_snapshots_from_excel(excel_file_path)
