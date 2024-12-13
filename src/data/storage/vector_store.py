from typing import List, Dict, Optional, Tuple
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http.models import Distance, VectorParams

from .base_storage import BaseStorage


class QdrantVectorStore(BaseStorage):
    """Qdrant-based vector storage"""

    def __init__(
            self,
            url: str,
            collection_name: str = "document_vectors",
            dimension: int = 768
    ):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.dimension = dimension

    async def initialize(self):
        """Initialize Qdrant collection"""
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print(f"Error initializing Qdrant collection: {e}")

    async def save(self, key: str, vector: np.ndarray) -> bool:
        """Save vector to Qdrant"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    rest.PointStruct(
                        id=hash(key),  # Convert key to numeric ID
                        vector=vector.tolist(),
                        payload={"document_id": key}
                    )
                ]
            )
            return True

        except Exception as e:
            print(f"Error saving vector: {e}")
            return False

    async def load(self, key: str) -> Optional[np.ndarray]:
        """Load vector from Qdrant"""
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[hash(key)]
            )
            if not result:
                return None
            return np.array(result[0].vector)

        except Exception as e:
            print(f"Error loading vector: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """Delete vector from Qdrant"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=rest.PointIdsList(
                    points=[hash(key)]
                )
            )
            return True

        except Exception as e:
            print(f"Error deleting vector: {e}")
            return False

    async def search(
            self,
            query_vector: np.ndarray,
            k: int = 5
    ) -> List[Tuple[str, float]]:
        """Search similar vectors"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector.tolist(),
                limit=k
            )

            return [
                (point.payload["document_id"], point.score)
                for point in results
            ]

        except Exception as e:
            print(f"Error searching vectors: {e}")
            return []