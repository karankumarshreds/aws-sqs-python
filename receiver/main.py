import json
import uuid
import boto3
from dotenv import load_dotenv
import os 
from time import sleep

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
SQS_QUEUE_URL = os.environ.get("SQS_URL")
POLLING_TIME_INTERVAL = 3

# Helper method to throw the generic error
def throw(message):
    raise Exception(f'****** ERROR ******: {message}')

# Create sqs client
sqs_client = boto3.client(
        'sqs',
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_ACCESS_KEY,
        region_name = 'ap-south-1',
    )

# Receiver logic
def poll():
    print("Polling...")
    response = sqs_client.receive_message(
        QueueUrl = SQS_QUEUE_URL,
        MaxNumberOfMessages = 1,
        WaitTimeSeconds = 0,
    )
    for message in response.get("Messages", []):
        msg = json.loads(message["Body"])
        structure_id = msg.get('structure_id')
        uuid = msg.get('session_uuid');
        receipt_handle = message['ReceiptHandle']

        print(f'structure_id: {structure_id} && uuid: {uuid}')
        try:
            sqs_client.delete_message(
                QueueUrl = SQS_QUEUE_URL,
                ReceiptHandle = receipt_handle,
            )
            print('Message consumed and cleaned successfully')
        except:
            throw('Could not delete the message after reading')



def main():
    while True:
        poll()
        sleep(1)

if __name__ == "__main__":
    main()