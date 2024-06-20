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
