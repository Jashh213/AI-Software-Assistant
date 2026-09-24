from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker

loader = DocumentLoader(".")
documents = loader.load_documents()

chunker = TextChunker()

chunks = chunker.chunk_documents(documents)

print(len(chunks))

print(chunks[0])