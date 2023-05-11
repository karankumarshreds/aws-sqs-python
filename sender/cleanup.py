import boto3
import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
SQS_QUEUE_URL = os.environ.get("SQS_URL")

sqs_client = boto3.client(
        'sqs',
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_ACCESS_KEY,
        region_name = 'ap-south-1',
    )
response = sqs_client.purge_queue(QueueUrl=SQS_QUEUE_URL)
if response.get('ResponseMetadata').get('HTTPStatusCode') != 200:
    raise Exception
else: 
    print("Cleanup successful")


