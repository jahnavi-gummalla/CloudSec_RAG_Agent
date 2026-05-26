from pathlib import Path

DOCS_PATH = Path("docs")

CHUNK_SIZE = 120

for file in DOCS_PATH.glob("*.txt"):
    print(f"\nReading File: {file.name}\n")

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = [
        content[i:i + CHUNK_SIZE]
        for i in range(0, len(content), CHUNK_SIZE)
    ]

    print(f"Total Chunks Created: {len(chunks)}\n")

    for index, chunk in enumerate(chunks):
        print(f"\n--- Chunk {index + 1} ---\n")
        print(chunk)