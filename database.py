import csv
import sqlite3

from models.borrowables.audio_book import AudioBook
from models.borrowables.book import Book
from models.borrowables.borrowable import Borrowable
from models.borrowables.periodical import Periodical


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create tables
        self.create_tables()
        self.insert_mocks_from_csv()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT,
                category TEXT,
                language TEXT,
                authors TEXT,
                year_published INTEGER,
                isbn TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_books (
                title TEXT,
                category TEXT,
                language TEXT,
                authors TEXT,
                year_published INTEGER,
                isbn TEXT,
                audio_format TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS periodicals (
                title TEXT,
                category TEXT,
                language TEXT,
                authors TEXT,
                year_published INTEGER
            )
        ''')

    def insert_books(self, books):
        for book in books:
            self.cursor.execute('''
                INSERT INTO books (title, category, language, authors, year_published, isbn)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (book.title, book.category, book.language, ', '.join(book.authors), book.year_published, book.isbn))
        self.conn.commit()

    def insert_audio_books(self, audio_books):
        for audio_book in audio_books:
            self.cursor.execute('''
                  INSERT INTO audio_books (title, category, language, authors, year_published, isbn, audio_format)
                  VALUES (?, ?, ?, ?, ?, ?, ?)
              ''', (audio_book.title, audio_book.category, audio_book.language,
                    ', '.join(audio_book.authors), audio_book.year_published,
                    audio_book.isbn, audio_book.audio_format))
        self.conn.commit()

    def insert_periodicals(self, periodicals):
        for periodical in periodicals:
            self.cursor.execute('''
                  INSERT INTO periodicals (title, category, language, authors, year_published)
                  VALUES (?, ?, ?, ?, ?)
              ''', (periodical.title, periodical.category, periodical.language,
                    ', '.join(periodical.authors), periodical.year_published))
        self.conn.commit()

    def get_books(self):
        self.cursor.execute('SELECT * FROM books')
        rows = self.cursor.fetchall()
        return [Book(row[0], row[1], row[2], row[3].split(', '), row[4], row[5]) for row in rows]

    def get_audio_books(self):
        self.cursor.execute('SELECT * FROM audio_books')
        rows = self.cursor.fetchall()
        return [AudioBook(row[0], row[1], row[2], row[3].split(', '), row[4], row[5], row[6]) for row in rows]

    def get_periodicals(self):
        self.cursor.execute('SELECT * FROM periodicals')
        rows = self.cursor.fetchall()
        return [Periodical(row[0], row[1], row[2], row[3].split(', '), row[4]) for row in rows]

    def get_borrowables(self) -> list[Borrowable]:
        return self.get_books() + self.get_audio_books() + self.get_periodicals()

    def insert_mocks_from_csv(self):
        # Insert mock data if tables are empty
        self.cursor.execute('SELECT COUNT(*) FROM books')
        if self.cursor.fetchone()[0] == 0:  # If the books table is empty
            self.insert_books_from_csv('mock_data/books.csv')

        self.cursor.execute('SELECT COUNT(*) FROM audio_books')
        if self.cursor.fetchone()[0] == 0:  # If the audio_books table is empty
            self.insert_audio_books_from_csv('mock_data/audio_books.csv')

        self.cursor.execute('SELECT COUNT(*) FROM periodicals')
        if self.cursor.fetchone()[0] == 0:  # If the periodicals table is empty
            self.insert_periodicals_from_csv('mock_data/periodicals.csv')

    def insert_books_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            books = []
            for row in reader:
                title, category, language, authors, year_published, isbn, _ = row
                authors = authors.split(', ')
                year_published = int(year_published) if year_published else None
                book = Book(title, category, language, authors, year_published, isbn)
                books.append(book)
            self.insert_books(books)
        self.conn.commit()

    def insert_audio_books_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            audio_books = []
            for row in reader:
                title, category, language, authors, year_published, isbn, audio_format = row
                authors = authors.split(', ')
                year_published = int(year_published) if year_published else None
                audio_book = AudioBook(title, category, language, authors, year_published, isbn, audio_format)
                audio_books.append(audio_book)
            self.insert_audio_books(audio_books)
        self.conn.commit()

    def insert_periodicals_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            periodicals = []
            for row in reader:
                title, category, language, authors, year_published, _, _ = row
                authors = authors.split(', ')
                year_published = int(year_published) if year_published else None
                periodical = Periodical(title, category, language, authors, year_published)
                periodicals.append(periodical)
            self.insert_periodicals(periodicals)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
