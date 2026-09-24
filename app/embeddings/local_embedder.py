from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Local Embedding Model using BAAI/bge-small-en-v1.5.

    Responsibilities
    ----------------
    - Generate embeddings for repository chunks
    - Generate embeddings for user queries

    Advantages
    ----------
    ✔ No API quota
    ✔ No internet after first download
    ✔ Fast
    ✔ Free
    """

    def __init__(self):

        print("Loading local embedding model...")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        print("Local embedding model loaded.")

    # =====================================================
    # Multiple Texts
    # =====================================================

    def embed_texts(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings.tolist()

    # =====================================================
    # Single Query
    # =====================================================

    def embed_query(
        self,
        text: str
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()