import json
import boto3
import os
from boto3.dynamodb.conditions import Attr
import configparser
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
    # Handle CORS preflight request
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
        response = table.scan(
            FilterExpression=Attr("available").eq(True)
        )
        logger.debug(f"Retrieved available slots: {response}")
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(response.get("Items", []))
        }
    except Exception as e:
        logger.exception("Error retrieving available slots")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }


