from double_linked_list import DoubleLinkedList
from users.borrower import Borrower


class BorrowerList(DoubleLinkedList[Borrower]):
    def search(self, username):
        current_node = self.head
        while current_node is not None:
            if current_node.data.username == username:
                return current_node.data
            current_node = current_node.next
        return None
