from models.borrowables.borrowable import Borrowable


class Book(Borrowable):
    def __init__(self, title, category, language, authors, year_published, isbn):
        super().__init__(title, category, language, authors, year_published)
        self.isbn = isbn

    def __str__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}"
