import pytest
import numpy as np
from src.data.loaders import Document

@pytest.fixture
def sample_document():
    return Document(
        id="test_doc_1",
        content="Test content",
        metadata={"source": "test"}
    )

@pytest.fixture
def sample_embedding():
    embedding = np.random.randn(768)
    return embedding / np.linalg.norm(embedding)
