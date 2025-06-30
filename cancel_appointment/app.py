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
    try:
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

        logger.debug("Received event: %s", json.dumps(event))    
        body = json.loads(event.get("body", "{}"))
        appointment_id = body.get("appointment_id")

        if not appointment_id:
            logger.error("Missing appointment_id in request body")
            raise ValueError("Missing appointment_id")

        appointments_table.update_item(
            Key={"appointment_id": appointment_id},
            UpdateExpression="SET #s = :status",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":status": "cancelled"}
        )
        logger.info("Appointment %s cancelled successfully", appointment_id)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "Appointment cancelled"})
        }

    except Exception as e:
        logger.error("Error cancelling appointment: %s", str(e))
        # Return a 500 error with the error message
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }

