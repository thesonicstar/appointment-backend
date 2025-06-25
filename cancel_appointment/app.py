import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
appointments_table = dynamodb.Table(os.environ["APPOINTMENTS_TABLE"])
slots_table = dynamodb.Table(os.environ["SLOTS_TABLE"])

def lambda_handler(event, context):
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        patient_id = claims.get("sub")

        body = json.loads(event["body"])
        appointment_id = body.get("appointment_id")

        # Get appointment
        response = appointments_table.get_item(Key={"appointment_id": appointment_id})
        appointment = response.get("Item")

        if not appointment or appointment["patient_id"] != patient_id:
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "Not authorized or appointment not found"})
            }

        # Mark appointment as cancelled
        appointments_table.update_item(
            Key={"appointment_id": appointment_id},
            UpdateExpression="SET #status = :val",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":val": "cancelled"}
        )

        # Set slot back to available
        slot_id = appointment["slot_id"]
        slots_table.update_item(
            Key={"slot_id": slot_id},
            UpdateExpression="SET available = :val",
            ExpressionAttributeValues={":val": True}
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Appointment cancelled"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
