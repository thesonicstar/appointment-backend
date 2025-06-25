import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    try:
        response = table.scan(
            FilterExpression=Attr("available").eq(True)
        )
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response.get("Items", []))
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# This code defines a Lambda function that retrieves available slots from a DynamoDB table.
# It scans the table for items where the 'available' attribute is True and returns them as a JSON response.
# If an error occurs, it returns a 500 status code with the error message.