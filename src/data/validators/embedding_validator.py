import numpy as np
from .base_validator import BaseValidator, ValidationResult


class EmbeddingValidator(BaseValidator):
    """Validator for embedding vectors"""

    def __init__(self, expected_dim: int = 768):
        self.expected_dim = expected_dim

    def validate(self, embedding: np.ndarray) -> ValidationResult:
        errors = []
        warnings = []

        # Type validation
        if not isinstance(embedding, np.ndarray):
            errors.append("Embedding must be a numpy array")
            return ValidationResult(False, errors, warnings)

        # Dimension validation
        if embedding.shape[-1] != self.expected_dim:
            errors.append(f"Expected embedding dimension {self.expected_dim}, got {embedding.shape[-1]}")

        # Numerical validation
        if not np.isfinite(embedding).all():
            errors.append("Embedding contains non-finite values")

        # Normalization check
        norm = np.linalg.norm(embedding)
        if not np.isclose(norm, 1.0, atol=1e-5):
            warnings.append("Embedding is not normalized")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
