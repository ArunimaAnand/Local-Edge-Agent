import faiss
import os
import yaml

from glob import glob
from sentence_transformers import SentenceTransformer

# read in the config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

knowledge_base_path = config.get("KNOWLEDGE_BASE_PATH", "knowledge/")
faiss_index_path = config.get("FAISS_INDEX_PATH", "faiss_index.index")
metadata_path = config.get("METADATA_PATH", "metadata.jsonl")

# load raw data from knowledge/*.md, knowledge/*.txt, and knowledge/*.pdf
# convert .md and .pdf to text
with open(knowledge_base_path, "r") as f:
    raw_texts = []
    
    for file_path in glob.glob(os.path.join(knowledge_base_path, "*")):
        if file_path.endswith(".md") or file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                raw_texts.append(f.read())
        elif file_path.endswith(".pdf"):
            # Placeholder for PDF conversion logic
            pass

# chunk the texts into 500-1000 token chunks. Improve later
chunk_size = 500  # tokens
chunks = []
for text in raw_texts:
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

# call embed_texts on all chunks
model = SentenceTransformer(config.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
embeddings = model.encode(chunks)

# build the faiss index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# save the faiss index and metadata
faiss.write_index(index, faiss_index_path)
with open(metadata_path, "w") as f:
    for i, chunk in enumerate(chunks):
        metadata = {
            "id": i,
            "text": chunk,
            "source": "knowledge_base"
        }
        f.write(yaml.dump([metadata]) + "\n")