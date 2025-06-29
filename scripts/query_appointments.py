import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Configuration
AWS_REGION = "eu-west-2"  # Adjust if needed
APPOINTMENTS_TABLE = "AppointmentsTable"  # Replace with your actual table name
PATIENT_ID = input("Enter patient_id to query: ")

# Create DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(APPOINTMENTS_TABLE)

def query_appointments(patient_id):
    try:
        response = table.query(
            IndexName="patient_id-index",
            KeyConditionExpression=Key("patient_id").eq(patient_id)
        )

        items = response.get("Items", [])
        print(f"\n✅ Found {len(items)} appointments for patient_id {patient_id}:\n")
        print(json.dumps(items, indent=2))
    except ClientError as e:
        print(f"❌ Error querying appointments: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    query_appointments(PATIENT_ID)
