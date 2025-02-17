from abc import ABC, abstractmethod
from typing import List

from models.author import Author


class Borrowable(ABC):
    def __init__(
            self,
            _id: str,
            title: str,
            category: str,
            language: str,
            authors: List[str],
            year_published: int,
    ):
        self.id = _id
        self.title = title
        self.category = category
        self.language = language
        self.authors = authors
        self.year_published = year_published

    def __str__(self):
        return f"{self.title}, Published in {self.year_published} in {self.language} by {', '.join(self.authors)} in the {self.category} category."
