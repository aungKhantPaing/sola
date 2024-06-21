from models.borrowables.borrowable import Borrowable


class AudioBook(Borrowable):
    def __init__(
            self,
            _id,
            title, category, language, authors, year_published, isbn,
            audio_format: str,
    ):
        super().__init__(_id, title, category, language, authors, year_published)
        self.isbn = isbn
        self.audio_format = audio_format

    def __str__(self):
        return f"Audio Book: {super().__str__()}"

    def get_detail(self):
        return (f"Audio Book Detail: {self.title}, Audio Format: {self.audio_format}, ISBN: {self.isbn}, "
                f"Published in {self.year_published} in {self.language} by {', '.join(self.authors)} "
                f"in the {self.category} category.")
