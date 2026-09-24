import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict


class VectorStore:
    """
    Production-ready FAISS Vector Store.

    Responsibilities:
    - Store embeddings
    - Store metadata
    - Search vectors
    - Save/Load index
    """

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        self.metadata: List[Dict] = []

    # =====================================================
    # Add Embeddings
    # =====================================================

    def add_embeddings(
        self,
        vectors: List[List[float]],
        metadata: List[Dict]
    ) -> None:


        vectors = np.array(vectors, dtype=np.float32)
        faiss.normalize_L2(vectors) #prebuilt normalization function
        self.index.add(vectors)
        self.metadata.extend(metadata)

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) ->  List[Dict]:
        if self.index.ntotal == 0:
            return []
        query = np.array([query_vector], dtype=np.float32)
        faiss.normalize_L2(query)
        scores, indices = self.index.search(query, top_k)
        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            chunk = self.metadata[idx].copy()
            results.append({
                "chunk": chunk,
                "score": float(score)
                })

        return results
    # =====================================================
    # Save
    # =====================================================

    def save(
        self,
        index_path="storage/index.faiss",
        metadata_path="storage/metadata.pkl"
    ) -> None:
        Path(index_path).parent.mkdir(
    parents=True,
    exist_ok=True
)
        faiss.write_index(
            self.index,
            index_path
        )

        with open(metadata_path, "wb") as f:

            pickle.dump(self.metadata, f)

    # =====================================================
    # Load
    # =====================================================

    @classmethod
    def load(
        cls,
        index_path="storage/index.faiss",
        metadata_path="storage/metadata.pkl"
    ) -> "VectorStore":

        index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:

            metadata = pickle.load(f)

        store = cls(index.d)

        store.index = index

        store.metadata = metadata

        return store

    # =====================================================
    # Stats
    # =====================================================

    def __len__(self):

        return self.index.ntotal