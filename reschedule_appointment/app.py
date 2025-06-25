import json
import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        patient_id = claims.get("sub")

        body = json.loads(event["body"])
        old_appointment_id = body.get("old_appointment_id")
        new_slot_id = body.get("new_slot_id")
        contact_email = body.get("contact_email", "")
        contact_phone = body.get("contact_phone", "")

        # Get old appointment
        old_appointment = appointments_table.get_item(Key={"appointment_id": old_appointment_id}).get("Item")
        if not old_appointment or old_appointment["patient_id"] != patient_id:
            return {"statusCode": 403, "body": json.dumps({"error": "Unauthorized or invalid appointment"})}

        # Cancel old appointment
        appointments_table.update_item(
            Key={"appointment_id": old_appointment_id},
            UpdateExpression="SET #status = :val",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":val": "cancelled"}
        )
        slots_table.update_item(
            Key={"slot_id": old_appointment["slot_id"]},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )

        # Check if new slot is available
        new_slot = slots_table.get_item(Key={"slot_id": new_slot_id}).get("Item")
        if not new_slot or not new_slot.get("available", False):
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

        slots_table.update_item(
            Key={"slot_id": new_slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": False}
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"new_appointment_id": new_appointment_id})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
# This code is a Lambda function that handles the rescheduling of appointments.
# It checks the user's authorization, cancels the old appointment, verifies the new slot's availability, and books the new appointment.