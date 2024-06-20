from models.borrowables.borrowable import Borrowable


class Periodical(Borrowable):
    def __str__(self):
        return f"Periodical: {self.title}, Year Published: {self.year_published}"
