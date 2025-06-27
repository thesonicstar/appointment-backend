import json
import boto3
import os
import uuid
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
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        logger.debug(f"Claims: {claims}")
        patient_id = claims.get("sub")
        logger.info(f"Patient ID: {patient_id}")    

        body = json.loads(event["body"])
        old_appointment_id = body.get("old_appointment_id")
        new_slot_id = body.get("new_slot_id")
        contact_email = body.get("contact_email", "")
        contact_phone = body.get("contact_phone", "")

        # Get old appointment
        old_appointment = appointments_table.get_item(Key={"appointment_id": old_appointment_id}).get("Item")
        logger.debug(f"Old appointment: {old_appointment}")
        if not old_appointment or old_appointment["patient_id"] != patient_id:
            logger.warning(f"Unauthorized access or invalid appointment: {old_appointment_id}")
            return {"statusCode": 403, "body": json.dumps({"error": "Unauthorized or invalid appointment"})}

        # Cancel old appointment
        appointments_table.update_item(
            Key={"appointment_id": old_appointment_id},
            UpdateExpression="SET #status = :val",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":val": "cancelled"}
        )
        logger.info(f"Cancelled old appointment: {old_appointment_id}")

        slots_table.update_item(
            Key={"slot_id": old_appointment["slot_id"]},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )
        logger.info(f"Marked old slot as available: {old_appointment['slot_id']}")

        # Check if new slot is available
        new_slot = slots_table.get_item(Key={"slot_id": new_slot_id}).get("Item")
        if not new_slot or not new_slot.get("available", False):
            logger.warning(f"New slot not available: {new_slot_id}")
            return {"statusCode": 400, "body": json.dumps({"error": "New slot not available"})}

        # Book new appointment
        new_appointment_id = str(uuid.uuid4())
        appointments_table.put_item(Item={
            "appointment_id": new_appointment_id,
            "slot_id": new_slot_id,
            "patient_id": patient_id,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "status": "booked"
        })
        logger.info(f"Booked new appointment: {new_appointment_id}")    

        slots_table.update_item(
            Key={"slot_id": new_slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": False}
        )
        logger.info(f"Marked new slot as unavailable: {new_slot_id}")

        # Return the new appointment ID
        logger.debug(f"New appointment ID: {new_appointment_id}")
        return {
            "statusCode": 200,
            "body": json.dumps({"new_appointment_id": new_appointment_id})
        }

    except Exception as e:
        logger.exception("Error in rescheduling appointment")
        logger.error(f"Error in rescheduling appointment: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
# This code is a Lambda function that handles the rescheduling of appointments.
# It checks the user's authorization, cancels the old appointment, verifies the new slot's availability, and books the new appointment.