import boto3

client = boto3.client('bedrock', region_name='us-east-1')  # or us-east-2
response = client.list_foundation_models(byOutputModality='EMBEDDING')

for model in response['modelSummaries']:
    print(model['modelId'])
