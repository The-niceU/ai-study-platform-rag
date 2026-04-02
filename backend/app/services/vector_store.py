import os
import json
import faiss
import numpy as np

INDEX_DIR = "faiss_index"
INDEX_PATH = os.path.join(INDEX_DIR, "chunks.index")
META_PATH = os.path.join(INDEX_DIR, "chunks_meta.json")


def ensure_index_dir():
    os.makedirs(INDEX_DIR, exist_ok=True)


def build_faiss_index(vectors: list[list[float]], metadata: list[dict]):
    ensure_index_dir()

    if not vectors:
        return

    dimension = len(vectors[0])
    index = faiss.IndexFlatIP(dimension)

    np_vectors = np.array(vectors, dtype="float32")
    index.add(np_vectors)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_faiss_index():
    if not os.path.exists(INDEX_PATH):
        return None
    return faiss.read_index(INDEX_PATH)


def load_metadata():
    if not os.path.exists(META_PATH):
        return []
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_similar(query_vector: list[float], top_k: int = 5):
    index = load_faiss_index()
    metadata = load_metadata()

    if index is None or not metadata:
        return []

    query = np.array([query_vector], dtype="float32")
    scores, indices = index.search(query, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1 or idx >= len(metadata):
            continue
        item = metadata[idx].copy()
        item["score"] = float(score)
        results.append(item)

    return results