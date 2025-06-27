import json
import boto3
import os
from boto3.dynamodb.conditions import Attr
import configparser  # For reading the config file
import logging

# Load config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Set up logging based on config
log_level_str = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger = logging.getLogger()
logger.setLevel(numeric_level)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    try:
        response = table.scan(
            FilterExpression=Attr("available").eq(True)
        )
        logger.debug(f"Retrieved available slots: {response}")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response.get("Items", []))
        }
    except Exception as e:
        logger.exception("Error retrieving available slots")
        logger.error(f"Error retrieving available slots: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# This code defines a Lambda function that retrieves available slots from a DynamoDB table.
# It scans the table for items where the 'available' attribute is True and returns them as a JSON response.
# If an error occurs, it returns a 500 status code with the error message.