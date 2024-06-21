from models.borrowables.borrowable import Borrowable


class Periodical(Borrowable):

    def __str__(self):
        return f"Periodical: {super().__str__()}"

    def get_detail(self):
        return (f"Periodical Detail: {self.title}, Year Published: {self.year_published}, "
                f"Language: {self.language}, Category: {self.category}, Authors: {', '.join(self.authors)}")
