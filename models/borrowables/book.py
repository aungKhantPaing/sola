from models.borrowables.borrowable import Borrowable


class Book(Borrowable):
    def __init__(self, _id, title, category, language, authors, year_published, isbn):
        super().__init__(_id, title, category, language, authors, year_published)
        self.isbn = isbn

    def __str__(self):
        return f"Book: {super().__str__()}"

    def get_detail(self):
        return (f"Book Detail: {self.title}, ISBN: {self.isbn}, Published in {self.year_published} in {self.language} "
                f"by {', '.join(self.authors)} in the {self.category} category.")
