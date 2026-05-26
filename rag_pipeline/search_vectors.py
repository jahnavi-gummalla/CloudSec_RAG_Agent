import pickle

import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/faiss_index.index")

with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

query = "How should we secure S3 buckets?"

query_embedding = model.encode([query])

k = 2

distances, indices = index.search(query_embedding, k)

print("\nUser Query:")
print(query)

print("\nTop Matching Chunks:\n")

for i in indices[0]:
    print(chunks[i])
    print("\n-------------------\n")