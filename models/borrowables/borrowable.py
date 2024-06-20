from abc import ABC, abstractmethod
from typing import List

from models.author import Author


class Borrowable(ABC):
    def __init__(
            self,
            title: str,
            category: str,
            language: str,
            authors: List[str],
            year_published: int,
    ):
        self.title = title
        self.category = category
        self.language = language
        self.authors = authors
        self.year_published = year_published
