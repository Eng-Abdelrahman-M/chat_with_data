import pytest
import numpy as np
from unittest.mock import Mock, AsyncMock

from src.data.loaders import Document
from src.data.manager import DataManager
from src.data.validators import ValidationResult

@pytest.fixture
async def mock_stores():
    document_store = Mock()
    document_store.save = AsyncMock()
    document_store.load = AsyncMock()
    
    vector_store = Mock()
    vector_store.save = AsyncMock()
    vector_store.search = AsyncMock()
    
    return document_store, vector_store

class TestDataManager:
    @pytest.mark.asyncio
    async def test_process_document(self, mock_stores):
        # Your test implementation here
        pass
