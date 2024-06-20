from datetime import datetime

from models.borrowables.borrowable import Borrowable


class BorrowedItem:
    def __init__(self, _id, borrowable_id: str, borrower_account_number: str, borrowed_date: datetime,
                 due_date: datetime,
                 return_date: datetime = None):
        self.id = _id
        self.borrowable_id = borrowable_id
        self.borrower_account_number = borrower_account_number
        self.borrowed_date = borrowed_date
        self.due_date = due_date
        self.return_date = return_date

    def get_fine(self):
        if datetime.now() > self.due_date:
            return (datetime.now() - self.due_date).days * 5
        return 0
