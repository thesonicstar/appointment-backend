import boto3
import os
import json
import logging
import configparser
from boto3.dynamodb.conditions import Key

# Load config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Logging
log_level_str = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)
logger = logging.getLogger()
logger.setLevel(numeric_level)

dynamodb = boto3.resource("dynamodb")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    try:
        # Use patient_id from query string (if not using Cognito authorizer)
        patient_id = event.get("queryStringParameters", {}).get("patient_id")
        if not patient_id:
            raise ValueError("Missing patient_id")

        # Query appointments table
        response = appointments_table.query(
            IndexName="patient_id-index",
            KeyConditionExpression=Key("patient_id").eq(patient_id)
        )

        appointments = response.get("Items", [])

        # Enrich each appointment with slot details
        for appointment in appointments:
            slot_id = appointment.get("slot_id")
            slot_data = slots_table.get_item(Key={"slot_id": slot_id}).get("Item")
            if slot_data:
                appointment["datetime"] = slot_data.get("datetime")
                appointment["doctor_id"] = slot_data.get("doctor_id")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(appointments)
        }

    except Exception as e:
        logger.exception("Error retrieving enriched appointments")
        logger.error(f"Error: {str(e)}")
        # Return a 500 error with the exception message
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
# This Lambda function retrieves appointments for a specific patient and enriches them with slot details.
# It uses the patient_id from the query string to query the appointments table and then retrieves slot