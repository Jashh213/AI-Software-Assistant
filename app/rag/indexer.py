from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker
from app.embeddings.local_embedder import LocalEmbedder
from app.rag.vector_store import VectorStore


class Indexer:

    def __init__(self, project_path: str):

        self.loader = DocumentLoader(project_path)
        self.chunker = TextChunker()
        self.embedder = LocalEmbedder()

        self.vector_store = None

    def build_index(
    self,
    index_path: str | None = None,
    metadata_path: str | None = None
    ):
        print("Loading documents...")
        documents = self.loader.load_documents()
        print(f"Loaded {len(documents)} documents")
        print("Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        print(f"Generated {len(chunks)} chunks")
        print("Generating embeddings...")
        texts = [chunk["text"] for chunk in chunks]
        vectors = self.embedder.embed_texts(texts)
        print(f"Generated {len(vectors)} embeddings")
        dimension = len(vectors[0])
        self.vector_store = VectorStore(dimension)
        print("Storing vectors in FAISS...")
        self.vector_store.add_embeddings(vectors, chunks)
        print("Index built successfully!")
        # Save only if paths are provided
        if index_path and metadata_path:
            print("Saving index to disk...")
            self.vector_store.save(
            index_path=index_path,
            metadata_path=metadata_path
        )

        print("Index saved.")
        return self.vector_store