from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def create_embedding(self, text):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )