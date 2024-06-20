import csv
import sqlite3

from models.borrowables.audio_book import AudioBook
from models.borrowables.book import Book
from models.borrowables.borrowable import Borrowable
from models.borrowables.periodical import Periodical
from models.borrowed_item import BorrowedItem
from models.users.admin import Admin
from models.users.borrower import Borrower


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create tables
        self.create_tables()
        self.insert_mocks_borrowables()
        self.insert_mocks_users()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
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
            CREATE TABLE IF NOT EXISTS users (
                type TEXT,
                username TEXT,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                account_number INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowed_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                borrowable_id INTEGER,
                borrower_account_number INTEGER,
                borrowed_date TEXT,
                due_date TEXT,
                return_date TEXT,
                FOREIGN KEY (borrowable_id) REFERENCES borrowables(id),
                FOREIGN KEY (borrower_account_number) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def insert_books(self, books):
        for book in books:
            self.cursor.execute('''
                    INSERT INTO borrowables (type, title, category, language, authors, year_published, isbn)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                'Book', book.title, book.category, book.language, ', '.join(book.authors), book.year_published,
                book.isbn))
        self.conn.commit()

    def insert_audio_books(self, audio_books):
        for audio_book in audio_books:
            self.cursor.execute('''
                    INSERT INTO borrowables (type, title, category, language, authors, year_published, isbn, audio_format)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                'AudioBook', audio_book.title, audio_book.category, audio_book.language, ', '.join(audio_book.authors),
                audio_book.year_published, audio_book.isbn, audio_book.audio_format))
        self.conn.commit()

    def insert_periodicals(self, periodicals):
        for periodical in periodicals:
            self.cursor.execute('''
                    INSERT INTO borrowables (type, title, category, language, authors, year_published)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                'Periodical', periodical.title, periodical.category, periodical.language, ', '.join(periodical.authors),
                periodical.year_published))
        self.conn.commit()

    def get_books(self):
        self.cursor.execute('SELECT * FROM borrowables WHERE type = "Book"')
        rows = self.cursor.fetchall()
        return [Book(row[2], row[3], row[4], row[5].split(', '), row[6], row[7]) for row in rows]

    def get_audio_books(self):
        self.cursor.execute('SELECT * FROM borrowables WHERE type = "AudioBook"')
        rows = self.cursor.fetchall()
        return [AudioBook(row[2], row[3], row[4], row[5].split(', '), row[6], row[7], row[8]) for row in rows]

    def get_periodicals(self):
        self.cursor.execute('SELECT * FROM borrowables WHERE type = "Periodical"')
        rows = self.cursor.fetchall()
        return [Periodical(row[2], row[3], row[4], row[5].split(', '), row[6]) for row in rows]

    def get_borrowables(self) -> list[Borrowable]:
        return self.get_books() + self.get_audio_books() + self.get_periodicals()

    def get_borrowers(self):
        self.cursor.execute('SELECT * FROM users WHERE type = "Borrower"')
        rows = self.cursor.fetchall()
        return [Borrower(row[1], row[2], row[3], row[4], row[5]) for row in rows]

    def get_borrowed_items(self):
        self.cursor.execute('SELECT * FROM borrowed_items')
        rows = self.cursor.fetchall()
        return [BorrowedItem(row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def insert_borrower(self, username, password, first_name, last_name):
        self.cursor.execute('''
            INSERT INTO users (type, username, password, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Borrower', username, password, first_name, last_name))
        self.conn.commit()

    def insert_borrowed_item(self, borrowable_id, borrower_account_number, borrowed_date, due_date, return_date):
        self.cursor.execute('''
            INSERT INTO borrowed_items (borrowable_id, borrower_account_number, borrowed_date, due_date, return_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (borrowable_id, borrower_account_number, borrowed_date,
              due_date, return_date))
        self.conn.commit()

        # Get the ID of the last inserted row
        last_row_id = self.cursor.lastrowid

        # Fetch the last inserted row
        self.cursor.execute('SELECT * FROM borrowed_items WHERE id = ?', (last_row_id,))
        row = self.cursor.fetchone()

        # Create a BorrowedItem object from the fetched row
        return BorrowedItem(row[1], row[2], row[3], row[4], row[5], row[6])

    def update_borrowed_item(self, borrowed_item: BorrowedItem):
        self.cursor.execute('''
            UPDATE borrowed_items
            SET borrowed_date = ?,
                due_date = ?,
                return_date = ?
            WHERE id = ?
        ''', (
            borrowed_item.borrowed_date, borrowed_item.due_date, borrowed_item.return_date, borrowed_item.id,))
        self.conn.commit()

    def update_borrower(self, borrower: Borrower):
        self.cursor.execute('''
            UPDATE users
            SET username = ?,
                first_name = ?,
                last_name = ?
            WHERE account_number = ?
        ''', (
            borrower.username, borrower.first_name, borrower.last_name, borrower.account_number))
        self.conn.commit()

    def delete_borrower(self, account_number):
        self.cursor.execute('''
            DELETE FROM users
            WHERE account_number = ?
        ''', (account_number,))
        self.conn.commit()

    def insert_mocks_borrowables(self):
        # Insert mock data if tables are empty
        self.cursor.execute('SELECT COUNT(*) FROM borrowables')
        if self.cursor.fetchone()[0] == 0:  # If the borrowables table is empty
            self.insert_borrowables_from_csv('mock_data/books.csv', 'Book')
            self.insert_borrowables_from_csv('mock_data/audio_books.csv', 'AudioBook')
            self.insert_borrowables_from_csv('mock_data/periodicals.csv', 'Periodical')

    def insert_mocks_users(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        if self.cursor.fetchone()[0] == 0:
            self.insert_borrower('user1', 'passw0rd', 'John', 'Doe', )
            self.insert_borrower('user2', 'passw0rd', 'Jane', 'Doe', )
            self.insert_borrower('user3', 'passw0rd', 'John', 'Smith')

    def insert_borrowables_from_csv(self, csv_file_path, borrowable_type):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            borrowables = []
            for row in reader:
                title, category, language, authors, year_published, isbn, audio_format = row
                authors = authors.split(', ')
                year_published = int(year_published) if year_published else None
                if borrowable_type == 'Book':
                    borrowable = Book(title, category, language, authors, year_published, isbn)
                elif borrowable_type == 'AudioBook':
                    borrowable = AudioBook(title, category, language, authors, year_published, isbn, audio_format)
                elif borrowable_type == 'Periodical':
                    borrowable = Periodical(title, category, language, authors, year_published)
                borrowables.append(borrowable)
            if borrowable_type == 'Book':
                self.insert_books(borrowables)
            elif borrowable_type == 'AudioBook':
                self.insert_audio_books(borrowables)
            elif borrowable_type == 'Periodical':
                self.insert_periodicals(borrowables)
        self.conn.commit()


def close_connection(self):
    self.conn.close()
