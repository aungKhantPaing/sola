from datetime import datetime, timedelta

from models.borrowables.borrowable import Borrowable


def get_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")


class BorrowedItem:
    def __init__(self, _id, borrowable_id: str, borrower_account_number: str, borrowed_date: str,
                 due_date: str = None,
                 return_date: str = None,
                 fine_paid: int = 0):
        self.id = _id
        self.borrowable_id = borrowable_id
        self.borrower_account_number = borrower_account_number
        self.borrowed_date = get_datetime(borrowed_date)
        self.due_date = get_datetime(due_date) if due_date is not None else self.borrowed_date + timedelta(days=7)
        self.return_date = get_datetime(return_date) if return_date is not None else None
        self._fine_paid = True if fine_paid == 1 else False


    @property
    def fine_paid(self) -> bool:
        return self._fine_paid

    def get_fine(self):
        if (self._fine_paid is False and
                self.return_date is not None and
                self.return_date > self.due_date):
            return (self.return_date - self.due_date).days * 10
        return 0

    def pay_fine(self):
        self._fine_paid = True

    def __str__(self):
        _str = f"Borrowed ID: {self.borrowable_id} on {self.borrowed_date.strftime('%Y-%m-%d')} " \
               f"due on {self.due_date.strftime('%Y-%m-%d')}"
        fine = self.get_fine()
        if fine > 0:
            _str += f" (Fine: ${fine})"
        return _str
