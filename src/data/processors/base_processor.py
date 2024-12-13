from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional
from ..loaders.base_loader import Document


class BaseProcessor(ABC):
    """Base class for all document processors"""

    @abstractmethod
    async def process(self, document: Document) -> Document:
        """Process a single document"""
        pass

    async def process_batch(self, documents: List[Document]) -> List[Document]:
        """Process multiple documents"""
        return [await self.process(doc) for doc in documents]