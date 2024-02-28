import boto3
import pandas as pd
from datetime import datetime, timedelta

def is_snapshot_old_enough(age_days):
    # Check if the age is greater than or equal to 100 days
    return age_days >= 105

def is_snapshot_in_use(snapshot_id):
    # Implement logic to check if snapshot is in use
    # This function can be modified based on your requirements
    ec2_client = boto3.client('ec2')
    
    # Check if any instances are using the snapshot as their root or data volume
    instances = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for volume in instance.get('BlockDeviceMappings', []):
                if volume.get('Ebs', {}).get('SnapshotId') == snapshot_id:
                    print(f"Snapshot {snapshot_id} is used by instance {instance['InstanceId']} as root or data volume")
                    return True
    
    # Check if the snapshot is used by any AMIs
    images = ec2_client.describe_images(
        Filters=[
            {'Name': 'block-device-mapping.snapshot-id', 'Values': [snapshot_id]}
        ]
    )
    for image in images['Images']:
        print(f"Snapshot {snapshot_id} is used by AMI {image['ImageId']}")
        return True
    
    return False

def display_old_snapshots_from_excel(excel_file_path):
    # Read Excel file using pandas
    snapshot_df = pd.read_excel(excel_file_path)
    
    # Iterate over rows in the dataframe
    for index, row in snapshot_df.iterrows():
        snapshot_id = row['Snapshot ID']
        region = row['Region']
        age_days = row['Age (Days)']
        usage_qty_gb = row['Usage Qty (GB)']
        monthly_cost = row['Monthly Cost ($)']
        
        # Check if the snapshot is older than or equal to 100 days and not in use
        if is_snapshot_old_enough(age_days) and not is_snapshot_in_use(snapshot_id):
            print(f"Snapshot ID: {snapshot_id}")
            print(f"Region: {region}")
            print(f"Age (Days): {age_days}")
            print(f"Usage Qty (GB): {usage_qty_gb}")
            print(f"Monthly Cost ($): {monthly_cost}")
            print("Not in use and older than or equal to 100 days")
            print("--------------------------------------------------")

if __name__ == "__main__":
    excel_file_path = 'infra_clean_up.xlsx'
    display_old_snapshots_from_excel(excel_file_path)
