import os
import math
import re
import logging
import numpy as np

logger = logging.getLogger(__name__)


class Embedder:
    """
    Lightweight, high-performance vector embedder.
    Runs with minimal memory (< 5MB RAM) so apps never hit Render 512MB or Vercel limits.
    """

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.model = None

        # Only load SentenceTransformer if explicitly enabled via environment variable
        if os.getenv("USE_HEAVY_TRANSFORMERS", "").lower() in ("true", "1", "yes"):
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as exc:
                logger.warning(f"SentenceTransformer not loaded: {exc}")

    def create_embedding(self, text: str) -> np.ndarray:
        if self.model:
            try:
                return self.model.encode(text, normalize_embeddings=True)
            except Exception as exc:
                logger.warning(f"Embedding encoding failed: {exc}")

        # Fast sublinear TF + hashed n-gram embedding
        clean_text = re.sub(r"[^\w\s]", " ", (text or "").lower())
        tokens = clean_text.split()
        vec = np.zeros(self.dim, dtype=np.float32)
        if not tokens:
            return vec

        # Unigrams + Bigrams for rich semantic and topical matching
        terms = tokens + [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        term_freq = {}
        for term in terms:
            term_freq[term] = term_freq.get(term, 0) + 1

        for term, freq in term_freq.items():
            # Sublinear TF: 1 + log(tf)
            weight = 1.0 + math.log(freq)
            h1 = abs(hash(term)) % self.dim
            h2 = abs(hash(term + "_ngram")) % self.dim
            vec[h1] += weight
            vec[h2] += weight * 0.5

        norm = np.linalg.norm(vec)
        return (vec / norm) if norm > 0 else vec