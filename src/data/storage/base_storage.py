from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class BaseStorage(ABC):
    """Base class for all storage implementations"""

    @abstractmethod
    async def save(self, key: str, data: Any) -> bool:
        """Save data to storage"""
        pass

    @abstractmethod
    async def load(self, key: str) -> Any:
        """Load data from storage"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete data from storage"""
        pass