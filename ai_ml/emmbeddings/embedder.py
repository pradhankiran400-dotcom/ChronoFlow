import os
import logging
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"
logger = logging.getLogger(__name__)


class Embedder:

    def __init__(self):
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as exc:
            logger.warning(f"SentenceTransformer failed to load: {exc}")

    def create_embedding(self, text):
        if self.model:
            try:
                return self.model.encode(text, normalize_embeddings=True)
            except Exception as exc:
                logger.warning(f"Embedding encoding failed: {exc}")

        # Fallback pseudo-embedding based on simple word hashing if ST is unavailable
        words = text.lower().split()
        vec = np.zeros(384, dtype=np.float32)
        for w in words:
            idx = abs(hash(w)) % 384
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec