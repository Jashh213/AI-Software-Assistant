from typing import List, Dict

from app.embeddings.local_embedder import LocalEmbedder
from app.rag.vector_store import VectorStore


class Retriever:
    """
    Production-ready Retriever.

    Responsibilities
    ----------------
    - Embed the user query
    - Retrieve candidate chunks from FAISS
    - Filter low similarity results
    - Ensure diversity across files
    """

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store
        self.embedder = LocalEmbedder()

    # =====================================================
    # Public API
    # =====================================================

    def retrieve(
        self,
        question: str,
        top_k: int = 10,
        similarity_threshold: float = 0.30,
        max_chunks_per_file: int = 2
    ) -> List[Dict]:

        # ---------------------------------------------
        # Step 1: Embed query
        # ---------------------------------------------

        query_vector = self.embedder.embed_query(question)

        # ---------------------------------------------
        # Step 2: Search FAISS
        # ---------------------------------------------

        search_results = self.vector_store.search(
    query_vector=query_vector,
    top_k=top_k
)

        # ---------------------------------------------
        # Debug
        # ---------------------------------------------

        print("\n========== SEARCH RESULTS ==========")

        for result in search_results:

            print(
                f"{result['score']:.4f}  "
                f"{result['chunk']['relative_path']}"
            )

        print("====================================\n")

        # ---------------------------------------------
        # Step 3: Filter by score
        # ---------------------------------------------

        filtered_results = self._filter_by_score(
            search_results,
            similarity_threshold
        )

        # ---------------------------------------------
        # Step 4: File diversity
        # ---------------------------------------------

        diverse_results = self._limit_chunks_per_file(
            filtered_results,
            max_chunks_per_file
        )

        return diverse_results

    # =====================================================
    # Similarity Filter
    # =====================================================

    def _filter_by_score(
        self,
        results: List[Dict],
        threshold: float
    ) -> List[Dict]:

        filtered = []

        for result in results:

            if result["score"] < threshold:
                continue

            chunk = result["chunk"].copy()

            chunk["score"] = result["score"]

            filtered.append(chunk)

        return filtered

    # =====================================================
    # Diversity Filter
    # =====================================================

    def _limit_chunks_per_file(
        self,
        chunks: List[Dict],
        max_chunks: int
    ) -> List[Dict]:

        selected = []

        file_counter = {}

        for chunk in chunks:

            filename = chunk["filename"]

            current = file_counter.get(
                filename,
                0
            )

            if current >= max_chunks:
                continue

            selected.append(chunk)

            file_counter[filename] = current + 1

        return selected