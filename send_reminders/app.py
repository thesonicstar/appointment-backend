import boto3
import os
import json
from datetime import datetime, timedelta, timezone
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
sns = boto3.client("sns")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])

def lambda_handler(event, context):
    try:
        now = datetime.now(timezone.utc)
        window_start = now + timedelta(hours=1)
        window_end = now + timedelta(hours=2)

        # Full scan (you can optimize with a GSI if needed)
        response = appointments_table.scan()
        items = response.get("Items", [])
        logger.debug(f"Retrieved {len(items)} items from the appointments table.")  

        reminders_sent = []
        logger.info(f"Checking appointments between {window_start} and {window_end}")

        for item in items:
            if item["status"] != "booked":
                continue

            appt_time = datetime.fromisoformat(item["datetime"])
            if window_start <= appt_time <= window_end:
                phone = item.get("contact_phone")
                email = item.get("contact_email")
                msg = f"Reminder: You have an appointment at {item['datetime']}."

                if phone:
                    sns.publish(
                        PhoneNumber=phone,
                        Message=msg
                    )
                    reminders_sent.append(phone)
        logger.info(f"Sent reminders to: {reminders_sent}")
        return {
            "statusCode": 200,
            "body": json.dumps({"reminders_sent": reminders_sent})
        }

    except Exception as e:
        logger.exception("Error sending reminders")
        logger.error(f"Error sending reminders: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
# This code is a simple AWS Lambda function that sends reminders for upcoming appointments.
# It scans a DynamoDB table for appointments within the next hour and sends SMS reminders using SNS.
# The function handles errors and returns a JSON response with the status of reminders sent.