from models.borrowed_item_list import BorrowedItemList
from models.users.user import User


class Borrower(User):
    def __init__(self, username, password, first_name, last_name, account_number):
        super().__init__(username, password, first_name, last_name)
        self._account_number = account_number

    @property
    def account_number(self):
        return self._account_number

    def has_unpaid_fines(self, borrowed_items_list: BorrowedItemList):
        return borrowed_items_list.has_unpaid_fines(self._account_number)

    def has_reached_borrow_limit(self, borrowed_items_list: BorrowedItemList):
        return borrowed_items_list.has_reached_borrow_limit(self._account_number)

    def get_borrowed_items(self, borrowed_items_list: BorrowedItemList):
        return borrowed_items_list.search(self._account_number)

    def get_unpaid_fines(self, borrowed_items_list: BorrowedItemList):
        return borrowed_items_list.search_unpaid_fines(self._account_number)

    def get_total_fines(self, borrowed_items_list: BorrowedItemList):
        return sum([item.get_fine() for item in self.get_unpaid_fines(borrowed_items_list)])

    def get_unreturned_items(self, borrowed_items_list: BorrowedItemList):
        return borrowed_items_list.search_unreturned_items(self._account_number)

    def display_info(self):
        return f"Borrower: {self.first_name} {self.last_name}, Account Number: {self._account_number}"

    __str__ = display_info
