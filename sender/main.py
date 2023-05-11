import json
import uuid
import boto3
from dotenv import load_dotenv
import sys
import os 

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
SQS_QUEUE_URL = os.environ.get("SQS_URL")

session_uuid =  uuid.uuid1()

# Helper method to throw the generic error
def throw(message):
    raise Exception(f'****** ERROR ******: {message}')

# Take the structure id from the cli
if len(sys.argv) < 2:
    throw('Please provide structure_id')
structure_id = sys.argv[1]

# Create sqs client
sqs_client = boto3.client(
        'sqs',
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_ACCESS_KEY,
        region_name = 'ap-south-1',
    )

# Sending the dummy message to the queue
payload = { 'structure_id': structure_id, 'session_uuid': str(session_uuid) }
response =  sqs_client.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(payload))

# Checking if the message was pushed on the queue successfully
if response.get('ResponseMetadata').get('HTTPStatusCode') != 200:
    raise Exception('Could not send message')
else:
    print('Message sent successfully to the queue')

print("Session id used", session_uuid)