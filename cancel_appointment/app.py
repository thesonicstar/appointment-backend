import json
import boto3
import os
import logging
import configparser  # For reading the config file

# Load config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Set up logging based on config
log_level_str = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger = logging.getLogger()
logger.setLevel(numeric_level)

dynamodb = boto3.resource("dynamodb")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])

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
    logger.debug(f"Received event: {json.dumps(event)}")

    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        patient_id = claims.get("sub")

        body = json.loads(event["body"])
        appointment_id = body.get("appointment_id")

        # Get appointment
        response = appointments_table.get_item(Key={"appointment_id": appointment_id})
        logger.info(f"Retrieved appointment: {response}")   
        appointment = response.get("Item")

        if not appointment or appointment["patient_id"] != patient_id:
            logger.warning(f"Unauthorized access or appointment not found for patient {patient_id} and appointment {appointment_id}.")
            return {
                "statusCode": 403,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Not authorized or appointment not found"})
            }

        # Mark appointment as cancelled
        appointments_table.update_item(
            Key={"appointment_id": appointment_id},
            UpdateExpression="SET #status = :val",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":val": "cancelled"}
        )
        logger.info(f"Appointment {appointment_id} cancelled successfully.")

        # Set slot back to available
        slot_id = appointment["slot_id"]
        slots_table.update_item(
            Key={"slot_id": slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )
        logger.info(f"Slot {slot_id} set back to available.")
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Appointment cancelled"})
        }

    except Exception as e:
        logger.exception("Error cancelling appointment")
        logger.error(f"Error cancelling appointment: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
