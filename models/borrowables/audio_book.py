from models.borrowables.borrowable import Borrowable


class AudioBook(Borrowable):
    def __init__(
            self,
            title, category, language, authors, year_published, isbn,
            audio_format: str,
    ):
        super().__init__(title, category, language, authors, year_published)
        self.isbn = isbn
        self.audio_format = audio_format

    def __str__(self):
        return f"AudioBook: {self.title}, Audio Format: {self.audio_format}"
