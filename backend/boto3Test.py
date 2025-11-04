from dataclasses import asdict
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

S3_BUCKET = "ml-vehiclefiles-bucket"
UPLOAD_PREFIX = "uploads/"
RESPONSE_PREFIX = "responses/"


s3 = boto3.resource(
                    's3',
                    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=  os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name='us-east-2'
                        )

                        
s3_client = boto3.client(
                        's3',
                        aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                        aws_secret_access_key=  os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name='us-east-2'
                        )

#list all bucket names
"""
all_buckets = s3_client.list_buckets()

for bucket in all_buckets["Buckets"]:
    print(bucket)
"""
s3.meta.client.upload_file("/Users/vibhas/Desktop/MLvehicle_code_scan/requirements.txt", S3_BUCKET, "uploads/testFile.txt")


