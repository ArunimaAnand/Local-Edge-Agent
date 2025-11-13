# Knowledge Context

This directory contains knowledge files that can be ingested by the local agent for retrieval-augmented generation (RAG). The agent can use these files to provide more accurate and context-aware responses.

## Supported File Types
- Markdown files (`.md`)
- Text files (`.txt`)
- PDF files (`.pdf`)

## Ingestion Process
1. **Loading**: The agent loads raw data from the knowledge files in this directory.
2. **Conversion**: Markdown and PDF files are converted to plain text.
3. **Chunking**: The texts are chunked into smaller segments (typically 500-1000 tokens) for better processing.
4. **Embedding**: Each chunk is embedded into a vector space using an embedding model.
5. **Indexing**: The embedded chunks are indexed using FAISS for efficient retrieval.
6. **Storage**: The FAISS index and associated metadata are saved for future use.

## Usage
To use the knowledge files, ensure that the ingestion process is completed. The agent will then be able to retrieve relevant information from these files when responding to queries.

```sh
python src/retrieval/ingest_knowledge.py
```