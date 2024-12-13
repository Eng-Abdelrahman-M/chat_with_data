class StorageConfig:
    MONGODB_URL = "mongodb://localhost:27017"
    QDRANT_URL = "http://localhost:6333"

    MONGODB_DATABASE = "llm_app"
    MONGODB_COLLECTION = "documents"

    QDRANT_COLLECTION = "document_vectors"
    VECTOR_DIMENSION = 768