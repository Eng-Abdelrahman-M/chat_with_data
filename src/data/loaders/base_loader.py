from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging


@dataclass
class Document:
    """Base document class that all dataset-specific documents will inherit from"""
    id: str
    content: str
    metadata: Dict[str, Any]


class BaseDatasetLoader(ABC):
    """Abstract base class for all dataset loaders"""

    def __init__(self, data_dir: str):
        """
        Initialize base loader

        Args:
            data_dir: Directory containing the dataset
        """
        self.data_dir = data_dir
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_documents(self, limit: Optional[int] = None) -> List[Document]:
        """
        Load documents from the dataset

        Args:
            limit: Maximum number of documents to load

        Returns:
            List of Document objects
        """
        pass

    @abstractmethod
    def load_by_filter(
            self,
            filter_dict: Dict[str, Any],
            limit: Optional[int] = None
    ) -> List[Document]:
        """
        Load documents matching specific criteria

        Args:
            filter_dict: Dictionary of field-value pairs to filter by
            limit: Maximum number of documents to return

        Returns:
            List of matching Document objects
        """
        pass

    def validate_document(self, document: Document) -> bool:
        """
        Validate a document's required fields

        Args:
            document: Document to validate

        Returns:
            True if valid, False otherwise
        """
        return all([
            document.id,
            document.content,
            isinstance(document.metadata, dict)
        ])

    def _log_error(self, message: str, *args, **kwargs) -> None:
        """
        Log an error message

        Args:
            message: Error message to log
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.error(message, *args, **kwargs)