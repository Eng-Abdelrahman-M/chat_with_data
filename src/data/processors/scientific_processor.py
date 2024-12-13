import re
from typing import Dict, List
from .base_processor import BaseProcessor
from ..loaders.base_loader import Document


class ScientificProcessor(BaseProcessor):
    """Process scientific documents (papers, articles)"""

    def __init__(self):
        self.section_patterns = {
            'abstract': r'abstract',
            'introduction': r'introduction|background',
            'methods': r'methods|methodology',
            'results': r'results',
            'discussion': r'discussion',
            'conclusion': r'conclusion'
        }

    async def process(self, document: Document) -> Document:
        """Process scientific document"""
        # Extract sections
        sections = self._extract_sections(document.content)

        # Process references
        references = self._extract_references(document.content)

        # Extract mathematical equations
        equations = self._extract_equations(document.content)

        # Update document
        document.metadata.update({
            'sections': sections,
            'references': references,
            'equation_count': len(equations),
            'document_type': 'scientific'
        })

        return document

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract standard scientific paper sections"""
        sections = {}
        for section, pattern in self.section_patterns.items():
            match = re.search(f'(?i){pattern}.*?\n(.*?)(?=\n\n|\Z)', text, re.DOTALL)
            if match:
                sections[section] = match.group(1).strip()
        return sections

    def _extract_references(self, text: str) -> List[str]:
        """Extract references from the document"""
        references = []
        ref_section = re.search(r'references.*?\n(.*?)(?=\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if ref_section:
            ref_text = ref_section.group(1)
            references = [ref.strip() for ref in ref_text.split('\n') if ref.strip()]
        return references

    def _extract_equations(self, text: str) -> List[str]:
        """Extract mathematical equations"""
        equations = re.findall(r'\$.*?\$', text)  # LaTeX math mode
        return equations
