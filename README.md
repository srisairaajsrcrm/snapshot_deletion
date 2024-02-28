Snapshot Check Utility Scripts

Introduction
These utility scripts, snapshot_xl.py and associated_only.py, are designed to manage AWS snapshots efficiently, specifically focusing on identifying and managing snapshots older than 90 days.
snapshot_xl.py
Purpose: This script checks AWS snapshots against an Excel sheet containing snapshot IDs. It identifies snapshots that are older than 90 days, listing both those present in the Excel sheet and those existing in our AWS console.
How it works:
1.	Reads the Excel sheet containing snapshot IDs.
2.	Compares the creation dates of snapshots in the AWS console with those in the Excel sheet.
3.	Prints snapshot IDs that are more than 90 days old, irrespective of whether they are listed in the Excel sheet or not.

Usage:

python snapshot_xl.py 


associated_only.py
Purpose: This script identifies snapshots that are more than or equal to 90 days old and are associated with EC2 instances for AMI creation.
How it works:
1.	Analyzes AWS snapshots to find those older than 90 days.
2.	Checks if these snapshots are associated with EC2 instances for AMI creation.
3.	Prints the snapshot IDs that meet these criteria.

Usage:

python associated_only.py 

Why It Matters
1.	Cost Optimization: Identifying and managing old snapshots helps in optimizing AWS costs by removing unnecessary storage.
2.	Security and Compliance: Regularly reviewing snapshots ensures compliance with data retention policies and enhances security by reducing the attack surface.
3.	Operational Efficiency: These scripts automate the process of snapshot management, saving time and effort for our team.
Conclusion
These scripts provide a streamlined approach to managing AWS snapshots, enhancing our operational efficiency and cost-effectiveness while ensuring compliance with security and data retention policies.

