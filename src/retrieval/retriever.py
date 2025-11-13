from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self, model):
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # returns [{
        #     "text": str,
        #     "source": str,
        #     "distance": float
        # }]
        return self.model.encode(texts).tolist()
    
class VectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index_path = index_path
        self.metadata_path = metadata_path

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5
    ) -> list[dict]:
        """Search the vector store for the top_k most similar vectors to the query_vector.
        
        Args:
            query_vector (list[float]): The embedding vector of the query.
            top_k (int): The number of top similar vectors to retrieve.
        Returns:
            list[dict]: A list of dictionaries containing the retrieved documents and their metadata.
        """
        # Placeholder implementation
        return []

class Retriever:
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        index_path: str = "faiss_index.index",
        metadata_path: str = "metadata.jsonl",
        top_k: int = 5
    ):
        self.embeddings = Embeddings(SentenceTransformer(embedding_model))
        self.vector_store = VectorStore(index_path=index_path, metadata_path=metadata_path)
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        """Retrieve relevant documents from the vector store based on the query.
        
        Args:
            query (str): The input query string.
        """
        query_vector = self.embeddings.embed_texts([query])[0]
        return self.vector_store.search(query_vector, self.top_k)