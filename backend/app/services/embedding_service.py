from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def encode_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def encode_query(text: str) -> list[float]:
    embedding = model.encode([text], normalize_embeddings=True)[0]
    return embedding.tolist()