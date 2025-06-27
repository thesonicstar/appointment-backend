import boto3
import os
import json
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

def lambda_handler(event, context):
    try:
        #claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
        claims = event["requestContext"]["authorizer"]["claims"]
        logger.info(f"Claims: {claims}")
        # Extract patient_id from claims (assuming 'sub' or 'email' is used)

        patient_id = claims.get("sub")  # or use 'email'

        # Query by patient_id (assuming GSI is used for this)
        response = appointments_table.query(
            IndexName="patient_id-index",  # we'll define this below
            KeyConditionExpression=boto3.dynamodb.conditions.Key("patient_id").eq(patient_id)
        )
        logger.debug(f"Query response: {response}")

        return {
            "statusCode": 200,
            "body": json.dumps(response.get("Items", [])),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        logger.exception("Error retrieving appointments")
        logger.error(f"Error retrieving appointments: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# Ensure the DynamoDB table has a GSI named 'patient_id-index'
# with 'patient_id' as the partition key.   