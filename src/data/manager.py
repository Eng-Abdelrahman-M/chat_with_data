from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

import numpy as np

from .loaders import BaseDatasetLoader, Document
from .storage import MongoDocumentStore, QdrantVectorStore
from .validators import DocumentValidator, EmbeddingValidator


class DataManager:
    """Manages the entire data flow: loading, validation, preprocessing, and storage"""

    def __init__(
            self,
            document_store: MongoDocumentStore,
            vector_store: QdrantVectorStore,
            loader: Optional[BaseDatasetLoader] = None
    ):
        self.document_store = document_store
        self.vector_store = vector_store
        self.loader = loader

        # Validators
        self.document_validator = DocumentValidator()
        self.embedding_validator = EmbeddingValidator()

        # Logging
        self.logger = logging.getLogger(__name__)

    async def process_document(self, document: Document) -> Optional[Document]:
        """Process a single document through the entire pipeline"""
        try:
            # Validate document
            validation_result = self.document_validator.validate(document)
            if not validation_result.is_valid:
                self.logger.error(f"Document validation failed: {validation_result.errors}")
                return None

            # Log warnings if any
            for warning in validation_result.warnings:
                self.logger.warning(f"Document warning: {warning}")

            # Preprocess document
            processed_doc = await self.preprocessing_pipeline.preprocess(document)

            # Validate embeddings
            embeddings = processed_doc.metadata['preprocessing_results'].get('embeddings')
            if embeddings:
                for i, emb in enumerate(embeddings):
                    emb_validation = self.embedding_validator.validate(emb)
                    if not emb_validation.is_valid:
                        self.logger.error(f"Embedding {i} validation failed: {emb_validation.errors}")
                        return None

            # Store document
            await self.document_store.save(processed_doc)

            # Store embeddings
            if embeddings:
                await self.vector_store.save(processed_doc.id, embeddings[0])  # Store first chunk embedding

            return processed_doc

        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            return None

    async def process_batch(
            self,
            documents: List[Document],
            batch_size: int = 100
    ) -> Dict[str, Any]:
        """Process a batch of documents"""
        results = {
            'successful': [],
            'failed': [],
            'total': len(documents)
        }

        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]

            for doc in batch:
                processed_doc = await self.process_document(doc)
                if processed_doc:
                    results['successful'].append(doc.id)
                else:
                    results['failed'].append(doc.id)

        return results

    async def load_and_process(
            self,
            limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Load documents from configured loader and process them"""
        if not self.loader:
            raise ValueError("No loader configured")

        # Load documents
        documents = await self.loader.load_documents(limit)

        # Process loaded documents
        return await self.process_batch(documents)

    async def search_similar(
            self,
            query_embedding: np.ndarray,
            k: int = 5
    ) -> List[Document]:
        """Search for similar documents using embeddings"""
        # Validate query embedding
        validation_result = self.embedding_validator.validate(query_embedding)
        if not validation_result.is_valid:
            self.logger.error(f"Query embedding validation failed: {validation_result.errors}")
            return []

        # Search vector store
        similar_docs = await self.vector_store.search(query_embedding, k)

        # Load full documents
        results = []
        for doc_id, score in similar_docs:
            doc = await self.document_store.load(doc_id)
            if doc:
                doc.metadata['similarity_score'] = score
                results.append(doc)

        return results


# Example usage
async def setup_data_pipeline():
    # Initialize components
    document_store = MongoDocumentStore("mongodb://localhost:27017")
    vector_store = QdrantVectorStore("http://localhost:6333")

    # Create manager
    manager = DataManager(
        document_store=document_store,
        vector_store=vector_store,
    )

    return manager
