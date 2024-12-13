from datetime import datetime
from typing import Dict, Any
from .base_processor import BaseProcessor
from ..loaders.base_loader import Document


class MetadataProcessor(BaseProcessor):
    """Process and enrich document metadata"""

    async def process(self, document: Document) -> Document:
        """Process document metadata"""
        # Enrich metadata
        metadata = self._enrich_metadata(document.metadata)

        # Add processing metadata
        metadata.update({
            'processed_at': datetime.utcnow().isoformat(),
            'content_length': len(document.content),
            'language': self._detect_language(document.content)
        })

        # Update document
        document.metadata = metadata

        return document

    def _enrich_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich existing metadata"""
        enriched = metadata.copy()

        # Add standard fields if missing
        if 'created_at' not in enriched:
            enriched['created_at'] = datetime.utcnow().isoformat()

        if 'source' not in enriched:
            enriched['source'] = 'unknown'

        return enriched

    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        # Add your language detection logic here
        # Could use langdetect or other libraries
        return 'en'  # Default to English for now