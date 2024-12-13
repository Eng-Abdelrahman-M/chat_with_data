from typing import List, Dict, Any
from .base_validator import BaseValidator, ValidationResult
from ..loaders.base_loader import Document


class DocumentValidator(BaseValidator):
    """Validator for Document objects"""

    def validate(self, document: Document) -> ValidationResult:
        errors = []
        warnings = []

        # Required fields validation
        if not document.id:
            errors.append("Document ID is required")

        if not document.content:
            errors.append("Document content cannot be empty")
        elif len(document.content) < 10:
            warnings.append("Document content is very short")

        if not isinstance(document.metadata, dict):
            errors.append("Metadata must be a dictionary")

        # Content validation
        if len(document.content) > 1_000_000:  # 1MB text limit
            errors.append("Document content exceeds maximum size")

        # Metadata validation
        if document.metadata:
            if 'source' not in document.metadata:
                warnings.append("Source information missing in metadata")
            if 'created_at' not in document.metadata:
                warnings.append("Creation date missing in metadata")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )