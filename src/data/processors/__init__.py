from .base_processor import BaseProcessor
from .text_processor import TextProcessor
from .scientific_processor import ScientificProcessor
from .metadata_processor import MetadataProcessor


# Chain multiple processors
class ProcessorChain:
    """Chain multiple processors together"""

    def __init__(self, processors: List[BaseProcessor]):
        self.processors = processors

    async def process(self, document: Document) -> Document:
        """Process document through all processors in chain"""
        for processor in self.processors:
            document = await processor.process(document)
        return document

    async def process_batch(self, documents: List[Document]) -> List[Document]:
        """Process multiple documents"""
        return [await self.process(doc) for doc in documents]