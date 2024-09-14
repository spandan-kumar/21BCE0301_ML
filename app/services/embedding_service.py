from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = 'distilbert-base-nli-mean-tokens'):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        return self.model.encode(text)

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)
