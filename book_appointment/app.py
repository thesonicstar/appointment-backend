import json
import boto3
import os
import uuid
import configparser
import logging

# Logging setup
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

log_level_str = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger = logging.getLogger()
logger.setLevel(numeric_level)

dynamodb = boto3.resource("dynamodb")
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    try:
        body = json.loads(event["body"])
        slot_id = body.get("slot_id")
        patient_id = body.get("patient_id")
        contact_email = body.get("contact_email", "")
        contact_phone = body.get("contact_phone", "")

        slot = slots_table.get_item(Key={"slot_id": slot_id}).get("Item")
        if not slot or not slot.get("available", False):
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Slot not available"})
            }

        appointment_id = str(uuid.uuid4())
        appointments_table.put_item(Item={
            "appointment_id": appointment_id,
            "slot_id": slot_id,
            "patient_id": patient_id,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "status": "booked"
        })

        slots_table.update_item(
            Key={"slot_id": slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": False}
        )

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"appointment_id": appointment_id})
        }

    except Exception as e:
        logger.exception("Booking failed")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
# This code is part of a serverless application that allows users to book appointments
# by selecting available time slots. It uses AWS DynamoDB to store slot and appointment data.