from app.rag.indexer import Indexer

indexer = Indexer(".")

vector_store = indexer.build_index()

print("\nFAISS index created successfully!")