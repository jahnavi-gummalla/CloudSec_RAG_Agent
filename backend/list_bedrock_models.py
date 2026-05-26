import os
import boto3
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

response = bedrock.list_foundation_models()

print("\nAvailable Text Models:\n")

for_model = response["modelSummaries"]

for model in for_model:
    model_id = model["modelId"]
    provider = model.get("providerName", "")
    output = model.get("outputModalities", [])

    if "TEXT" in output and provider in ["Amazon", "Anthropic"]:
        print(provider, "=>", model_id)