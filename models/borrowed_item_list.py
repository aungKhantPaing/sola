from models.double_linked_list import DoubleLinkedList
from models.borrowed_item import BorrowedItem


class BorrowedItemList(DoubleLinkedList[BorrowedItem]):
    def search(self, borrower_account_number):
        borrowed_items = []
        current_node = self.head
        while current_node is not None:
            if current_node.data.borrower_account_number == borrower_account_number:
                borrowed_items.append(current_node.data)
            current_node = current_node.next
        return borrowed_items

    def search_unpaid_fines(self, borrower_account_number):
        borrowed_items = []
        current_node = self.head
        while current_node is not None:
            if (current_node.data.borrower_account_number == borrower_account_number and
                    current_node.data.get_fine() > 0):
                borrowed_items.append(current_node.data)
            current_node = current_node.next
        return borrowed_items

    def has_unpaid_fines(self, borrower_account_number):
        current_node = self.head
        while current_node is not None:
            if (current_node.data.borrower_account_number == borrower_account_number and
                    current_node.data.get_fine() > 0):
                return True
            current_node = current_node.next
        return False

    def has_reached_borrow_limit(self, borrower_account_number):
        current_node = self.head
        borrowed_count = 0
        while current_node is not None and borrowed_count < 8:
            if (current_node.data.borrower_account_number == borrower_account_number
                    and current_node.data.return_date is None):
                borrowed_count += 1
            current_node = current_node.next
        return borrowed_count == 8

    def search_unreturned_items(self, borrower_account_number):
        borrowed_items = []
        current_node = self.head
        while current_node is not None:
            if (current_node.data.borrower_account_number == borrower_account_number and
                    current_node.data.return_date is None):
                borrowed_items.append(current_node.data)
            current_node = current_node.next
        return borrowed_items

    def search_returned_items(self, borrower_account_number):
        borrowed_items = []
        current_node = self.head
        while current_node is not None:
            if (current_node.data.borrower_account_number == borrower_account_number and
                    current_node.data.return_date is not None):
                borrowed_items.append(current_node.data)
            current_node = current_node.next
        return borrowed_items

    def is_item_borrowed(self, item_id):
        current_node = self.head
        while current_node is not None:
            if current_node.data.borrowable_id == item_id and current_node.data.return_date is None:
                return True
            current_node = current_node.next
        return False
