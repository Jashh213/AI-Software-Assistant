from app.rag.loader import DocumentLoader

loader = DocumentLoader(".")

documents = loader.load_documents()

print(f"\nLoaded {len(documents)} documents\n")

print(documents[0])