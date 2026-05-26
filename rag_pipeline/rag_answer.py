import pickle

import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/faiss_index.index")

with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

query = "How should we secure S3 buckets?"

query_embedding = model.encode([query])

distances, indices = index.search(query_embedding, 2)

retrieved_context = []

for i in indices[0]:
    retrieved_context.append(chunks[i])

print("\nQuestion:")
print(query)

print("\nRAG Answer:")
print("Based on the retrieved AWS security notes, S3 buckets should be secured by blocking public access, enabling bucket versioning, using server-side encryption, carefully configuring bucket policies, and monitoring access logs.")

print("\nRetrieved Context Used:")
for context in retrieved_context:
    print("\n---")
    print(context)