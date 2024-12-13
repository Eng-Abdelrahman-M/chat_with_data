from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
from datetime import datetime

from .base_storage import BaseStorage
from ..loaders.base_loader import Document


class MongoDocumentStore(BaseStorage):
    """MongoDB-based document storage"""

    def __init__(self, connection_url: str, database: str = "llm_app", collection: str = "documents"):
        self.client = AsyncIOMotorClient(connection_url)
        self.db = self.client[database]
        self.collection = self.db[collection]

    async def initialize(self):
        """Initialize indexes"""
        indexes = [
            IndexModel([("id", ASCENDING)], unique=True),
            IndexModel([("metadata.type", ASCENDING)]),
            IndexModel([("created_at", ASCENDING)])
        ]
        await self.collection.create_indexes(indexes)

    async def save(self, document: Document) -> bool:
        """Save document to MongoDB"""
        try:
            doc_dict = {
                "id": document.id,
                "content": document.content,
                "metadata": document.metadata,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            await self.collection.update_one(
                {"id": document.id},
                {"$set": doc_dict},
                upsert=True
            )
            return True

        except Exception as e:
            print(f"Error saving document: {e}")
            return False

    async def load(self, document_id: str) -> Optional[Document]:
        """Load document from MongoDB"""
        try:
            doc_dict = await self.collection.find_one({"id": document_id})
            if not doc_dict:
                return None

            return Document(
                id=doc_dict["id"],
                content=doc_dict["content"],
                metadata=doc_dict["metadata"]
            )

        except Exception as e:
            print(f"Error loading document: {e}")
            return None

    async def delete(self, document_id: str) -> bool:
        """Delete document from MongoDB"""
        try:
            result = await self.collection.delete_one({"id": document_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False