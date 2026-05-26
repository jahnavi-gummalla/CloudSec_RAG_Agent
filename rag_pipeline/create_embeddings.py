import os
import pickle
from pathlib import Path

import boto3
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
VECTOR_STORE_PATH = Path("vector_store")
CHUNK_SIZE = 120

VECTOR_STORE_PATH.mkdir(exist_ok=True)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

model = SentenceTransformer("all-MiniLM-L6-v2")

all_chunks = []

response = s3.list_objects_v2(Bucket=BUCKET_NAME)

for obj in response.get("Contents", []):
    key = obj["Key"]

    if key.endswith(".txt"):
        print(f"Reading from S3: {key}")

        file_object = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        content = file_object["Body"].read().decode("utf-8")

        chunks = [
            content[i:i + CHUNK_SIZE]
            for i in range(0, len(content), CHUNK_SIZE)
        ]

        all_chunks.extend(chunks)

embeddings = model.encode(all_chunks)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "vector_store/faiss_index.index")

with open("vector_store/chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print(f"Total Chunks Stored: {len(all_chunks)}")
print(f"Embedding Dimension: {dimension}")
print("FAISS vector store created from S3 documents successfully.")