import boto3
import json

# Replace this with your actual DynamoDB table name
APPOINTMENTS_TABLE = "AppointmentsTable"

# Initialize DynamoDB resource (uses default AWS credentials/profile/environment)
dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table(APPOINTMENTS_TABLE)

def scan_appointments():
    print(f"Scanning table: {APPOINTMENTS_TABLE}")
    try:
        response = table.scan()
        items = response.get("Items", [])
        print(json.dumps(items, indent=2))
    except Exception as e:
        print(f"Error scanning table: {e}")

if __name__ == "__main__":
    scan_appointments()
# This script scans the DynamoDB table for all appointments and prints them in a formatted JSON output.
# Make sure to replace "AppointmentsTable" with the actual name of your DynamoDB