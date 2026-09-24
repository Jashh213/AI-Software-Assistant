from app.embeddings.gemini_embedder import GeminiEmbedder

embedder = GeminiEmbedder()

vector = embedder.embed_text(
    "Retrieval Augmented Generation"
)

print(type(vector))
print(len(vector))
print(vector[:10])