
import boto3
from botocore.exceptions import ClientError

# Replace these with your actual AWS access key and secret access key
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'
bucket_name = 'tsystem'
file_key = 'testdatabase/file.txt'

# Create a Boto3 S3 client using your credentials
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


try:
    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Print object keys
    print(f"List of objects in bucket '{bucket_name}':")
    for obj in response.get('Contents', []):
        print(obj['Key'])
except Exception as e:
    print("An error occurred:", e)


try:
    # Use head_object to check if the file exists
    s3.head_object(Bucket=bucket_name, Key=file_key)
    print(f"File '{file_key}' exists in the bucket '{bucket_name}'.")
except ClientError as e:
    if e.response['Error']['Code'] == '404':
        print(f"File '{file_key}' does not exist in the bucket '{bucket_name}'.")
    else:
        print("An error occurred:", e)