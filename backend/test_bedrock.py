import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

prompt = """
Explain AWS S3 bucket security best practices in simple terms.
"""

body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 300,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = bedrock.invoke_model(
    modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    body=json.dumps(body)
)

response_body = json.loads(response["body"].read())

print("\nBedrock Response:\n")

print(response_body["content"][0]["text"])