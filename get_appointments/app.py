import boto3
import os
import json

dynamodb = boto3.resource("dynamodb")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])

def lambda_handler(event, context):
    try:
        #claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        claims = event["requestContext"]["authorizer"]["claims"]

        patient_id = claims.get("sub")  # or use 'email'

        # Query by patient_id (assuming GSI is used for this)
        response = appointments_table.query(
            IndexName="patient_id-index",  # we'll define this below
            KeyConditionExpression=boto3.dynamodb.conditions.Key("patient_id").eq(patient_id)
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", [])),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# Ensure the DynamoDB table has a GSI named 'patient_id-index'
# with 'patient_id' as the partition key.   