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