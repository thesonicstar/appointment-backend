import json
import boto3
import os
import uuid

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

        return {
            "statusCode": 201,
            "body": json.dumps({"appointment_id": appointment_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
