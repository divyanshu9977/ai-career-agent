# Optional semantic matcher. Install requirements-ai.txt to enable.
# The app continues to work with TF-IDF if these packages/model are unavailable.
def semantic_scores(query: str, documents: list[str]):
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vectors = model.encode([query] + documents, normalize_embeddings=True)
    return cosine_similarity([vectors[0]], vectors[1:]).flatten().tolist()
