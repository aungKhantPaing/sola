from models.double_linked_list import DoubleLinkedList
from models.users.borrower import Borrower


class BorrowerList(DoubleLinkedList[Borrower]):
    def search(self, username):
        current_node = self.head
        while current_node is not None:
            if current_node.data.username == username:
                return current_node.data
            current_node = current_node.next
        return None

    def search_by_account_number(self, account_number):
        current_node = self.head
        while current_node is not None:
            if str(current_node.data.account_number) == str(account_number):
                return current_node.data
            current_node = current_node.next
        return None

    def remove_by_account_number(self, account_number):
        current_node = self.head
        current_index = 0
        while current_node is not None:
            if str(current_node.data.account_number) == str(account_number):
                self.remove(current_index)
                return True
            current_node = current_node.next
            current_index += 1
        return False


