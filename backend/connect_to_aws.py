
import boto3
import datetime
from botocore.exceptions import ClientError

# Replace these with your actual AWS access key and secret access key
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'
bucket_name = 'tsystem'
file_key = 'testdatabase/customer.parquet'

# Create a Boto3 S3 client using your credentials
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def process_dttm():
    dttm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'{dttm} [INFO] :'

def check_objects_in_bucket():
    log = []
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        # Print object keys
        log += [f"{process_dttm()} Connection successful", '---']
        log.append(f"{process_dttm()} List of objects in bucket '{bucket_name}':")  
        for obj in response.get('Contents', []):
            log.append(f"{process_dttm()} {obj['Key']}")
            
    except Exception as e:
        log.append(f"{process_dttm()} An error occurred: {e}")

    return log

def check_databases():
    log = []

    try:
        # Use head_object to check if the file exists
        s3.head_object(Bucket=bucket_name, Key=file_key)
        log.append(f"{process_dttm()} File '{file_key}' exists in the bucket '{bucket_name}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            log.append(f"{process_dttm()} File '{file_key}' does not exist in the bucket '{bucket_name}'.")
        else:
            log.append(f"{process_dttm()} An error occurred: {e}")

    return log

