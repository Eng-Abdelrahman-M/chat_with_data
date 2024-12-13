import pytest
from src.data.manager import DataManager

@pytest.mark.integration
class TestIntegration:
    @pytest.mark.asyncio
    async def test_complete_pipeline(self):
        # Your integration test here
        pass
