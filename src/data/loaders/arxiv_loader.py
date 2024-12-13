# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""arXiv Dataset."""

import json
import os
from pathlib import Path
from typing import Dict, Iterator, Optional
from dataclasses import dataclass

from .base_loader import BaseDatasetLoader, Document



@dataclass
class ArxivDocument(Document):
    """ArXiv specific document class"""
    submitter: str
    authors: str
    title: str
    comments: str
    journal_ref: str
    doi: str
    report_no: str
    categories: str
    license: str
    abstract: str
    update_date: str


class ArxivLoader(BaseDatasetLoader):
    """Loader for ArXiv dataset"""

    # Class constants
    FILENAME = "arxiv-metadata-oai-snapshot.json"
    VERSION = "1.1.0"

    def __init__(self, data_dir: str):
        """
        Initialize ArXiv loader

        Args:
            data_dir: Directory containing the ArXiv dataset file
        """
        super().__init__(data_dir)
        self.file_path = Path(data_dir) / self.FILENAME

    @property
    def download_instructions(self) -> str:
        """Instructions for downloading the dataset"""
        return """
        To use this loader:
        1. Go to https://www.kaggle.com/Cornell-University/arxiv
        2. Download the dataset (will be named archive.zip)
        3. Extract the arxiv-metadata-oai-snapshot.json file
        4. Place it in your specified data directory
        """

    def _validate_file(self) -> None:
        """Validate that the dataset file exists"""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dataset file not found at {self.file_path}. "
                f"Please download the dataset first.\n{self.download_instructions}"
            )

    def _parse_entry(self, entry: Dict) -> ArxivDocument:
        """Parse a single JSON entry into an ArxivDocument"""
        return ArxivDocument(
            id=entry["id"],
            content=entry["abstract"],  # Using abstract as main content
            metadata={
                "source": str(self.file_path),
                "version": self.VERSION
            },
            submitter=entry["submitter"],
            authors=entry["authors"],
            title=entry["title"],
            comments=entry["comments"],
            journal_ref=entry["journal-ref"],
            doi=entry["doi"],
            report_no=entry["report-no"],
            categories=entry["categories"],
            license=entry["license"],
            abstract=entry["abstract"],
            update_date=entry["update_date"]
        )

    def _load_entries(self) -> Iterator[Dict]:
        """Load entries from the JSON file"""
        with open(self.file_path, encoding="utf8") as f:
            for line in f:
                yield json.loads(line)

    def load_documents(self, limit: Optional[int] = None) -> list[ArxivDocument]:
        """
        Load ArXiv documents

        Args:
            limit: Maximum number of documents to load

        Returns:
            List of ArxivDocument objects
        """
        self._validate_file()

        documents = []
        for i, entry in enumerate(self._load_entries()):
            if limit and i >= limit:
                break

            try:
                document = self._parse_entry(entry)
                documents.append(document)
            except Exception as e:
                self.logger.error(f"Error parsing entry {i}: {str(e)}")
                continue

        return documents

    def load_by_filter(
            self,
            filter_dict: Dict[str, str],
            limit: Optional[int] = None
    ) -> list[ArxivDocument]:
        """
        Load documents matching specific criteria

        Args:
            filter_dict: Dictionary of field-value pairs to filter by
            limit: Maximum number of documents to return

        Returns:
            List of matching ArxivDocument objects
        """
        documents = []

        for i, entry in enumerate(self._load_entries()):
            matches = all(
                entry.get(key, "") == value
                for key, value in filter_dict.items()
            )

            if matches:
                try:
                    document = self._parse_entry(entry)
                    documents.append(document)

                    if limit and len(documents) >= limit:
                        break
                except Exception as e:
                    self.logger.error(f"Error parsing entry {i}: {str(e)}")
                    continue

        return documents