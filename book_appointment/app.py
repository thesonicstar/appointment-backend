import json
import boto3
import os
import uuid
import logging
import configparser

# Load config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Set up logging based on config
log_level_str = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger = logging.getLogger()
logger.setLevel(numeric_level)
# Initialize DynamoDB resources
# Ensure that the environment variables SLOTS_TABLE and APPOINTMENTS_TABLE are set

dynamodb = boto3.resource("dynamodb")
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        patient_id = claims.get("sub")  # get user ID from Cognito token

        body = json.loads(event["body"])
        slot_id = body.get("slot_id")
        contact_email = body.get("contact_email", "")
        contact_phone = body.get("contact_phone", "")

        # Check if slot is available
        slot = slots_table.get_item(Key={"slot_id": slot_id}).get("Item")
        if not slot or not slot.get("available", False):
            logger.info(f"Slot {slot_id} not available for booking.")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Slot not available"})
            }

        # Create appointment record
        appointment_id = str(uuid.uuid4())
        appointments_table.put_item(Item={
            "appointment_id": appointment_id,
            "slot_id": slot_id,
            "patient_id": patient_id,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "status": "booked"
        })

        # Update slot to unavailable
        slots_table.update_item(
            Key={"slot_id": slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": False}
        )
        logger.info(f"Appointment {appointment_id} booked successfully for slot {slot_id}.")
        return {
            "statusCode": 201,
            "body": json.dumps({"appointment_id": appointment_id})
        }

    except Exception as e:
        logger.exception("Error booking appointment")
        logger.error(f"Error booking appointment: {str(e)}")
        # Return error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
