from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class BaseValidator(ABC):
    """Base class for all validators"""

    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """Validate data and return results"""
        pass