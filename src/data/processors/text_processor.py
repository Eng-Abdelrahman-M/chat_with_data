import re
from typing import List
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from .base_processor import BaseProcessor
from ..loaders.base_loader import Document


class TextProcessor(BaseProcessor):
    """Process text content of documents"""

    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    async def process(self, document: Document) -> Document:
        """Process document text"""
        # Clean text
        cleaned_text = self._clean_text(document.content)

        # Tokenize
        sentences = self._tokenize_sentences(cleaned_text)
        words = self._tokenize_words(cleaned_text)

        # Update document
        document.content = cleaned_text
        document.metadata.update({
            'sentence_count': len(sentences),
            'word_count': len(words),
            'processed': True
        })

        return document

    def _clean_text(self, text: str) -> str:
        """Clean text content"""
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def _tokenize_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        return sent_tokenize(text)

    def _tokenize_words(self, text: str) -> List[str]:
        """Split text into words and remove stopwords"""
        words = word_tokenize(text)
        return [word for word in words if word.lower() not in self.stop_words]