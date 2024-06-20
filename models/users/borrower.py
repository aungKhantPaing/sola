from models.users.user import User


class Borrower(User):
    def __init__(self, username, password, first_name, last_name, account_number):
        super().__init__(username, password, first_name, last_name)
        self._account_number = account_number
        self._rented_items = []

    @property
    def account_number(self):
        return self._account_number

    @property
    def rented_items(self):
        return self._rented_items.copy()

    def rent_item(self, item):
        self._rented_items.append(item)

    def return_item(self, item):
        self._rented_items.remove(item)

    def display_info(self):
        return f"Borrower: {self.first_name} {self.last_name}, Account Number: {self._account_number}"
