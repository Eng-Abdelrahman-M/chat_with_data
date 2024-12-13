import pytest
from src.data.validators import DocumentValidator, EmbeddingValidator

class TestDocumentValidator:
    def test_validate_document(self, sample_document):
        validator = DocumentValidator()
        result = validator.validate(sample_document)
        assert result.is_valid
