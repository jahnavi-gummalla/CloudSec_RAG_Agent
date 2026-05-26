import json
import os
import pickle

import boto3
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/faiss_index.index")

with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def generate_bedrock_answer(question, context):
    prompt = f"""
You are an AWS cloud security assistant.

Answer the user's question using only the context below.
If the answer is not found in the context, say you do not have enough information.

Context:
{context}

Question:
{question}
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
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
    return response_body["content"][0]["text"]


def get_rag_answer(question: str):
    question_embedding = model.encode([question])

    distances, indices = index.search(question_embedding, 2)

    retrieved_context = [chunks[i] for i in indices[0]]

    context_text = "\n\n".join(retrieved_context)

    answer = generate_bedrock_answer(question, context_text)

    return {
        "question": question,
        "answer": answer,
        "retrieved_context": retrieved_context
    }