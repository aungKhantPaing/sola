from typing import Generic, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    next: 'Node[T]' = None
    prev: 'Node[T]' = None

    def __init__(self, data: T):
        self.data = data

    def __str__(self):
        return str(self.data)


class DoubleLinkedList(Generic[T]):
    head: Node[T] = None
    tail: Node[T] = None
    size = 0

    def append(self, data):
        """Create a new node and append to linked list"""
        new_node = Node(data)

        if self.head is None:
            #  h
            # [*]
            #  t
            self.head = new_node
            self.tail = new_node
        else:
            #  h             t     t.next
            # [*] -> ... -> [*]
            # [*] -> ... -> [*] -> new_node
            self.tail.next = new_node
            # [*] -> ... -> [*] <-> new_node
            new_node.prev = self.tail
            #  h                       t
            # [*] -> ... -> [*] -> new_node
            self.tail = new_node

        self.size += 1

        return self

    def at(self, position):
        if position < self.size / 2:
            current_node = self.head
            for i in range(position):
                current_node = current_node.next
        else:
            current_node = self.tail
            for i in range(position):
                current_node = current_node.prev
        return current_node

    def pop(self):
        """Remove and return the last item in the linked list"""
        if self.size > 0:
            removed_node = self.tail
            self.size -= 1
            self.tail = self.tail.prev
            return removed_node
        else:
            return None

    def shift(self):
        """Remove and return the first item in the linked list"""
        if self.size > 0:
            removed_node = self.head
            self.size -= 1
            self.head = self.head.next
            # removed_node.next = None
            return removed_node
        else:
            return None

    def insert(self, position, data):
        """Insert new item at the specified position of linked list"""
        if position <= 0:
            self.prepend(data)
        elif position >= self.size:
            self.append(data)
        else:
            new_node = Node(data)
            current_node = self.head
            for i in range(position - 1):
                current_node = current_node.next
            new_node.next = current_node.next
            current_node.next = new_node
            self.size += 1

    def prepend(self, data):
        """Create a new node and add from the head"""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

        self.size += 1

    def remove(self, position):
        node_to_remove = self.at(position)
        if node_to_remove is None:
            return None
        else:
            if node_to_remove.prev is not None:
                node_to_remove.prev.next = node_to_remove.next
            else:
                self.head = node_to_remove.next

            if node_to_remove.next is not None:
                node_to_remove.next.prev = node_to_remove.prev
            else:
                self.tail = node_to_remove.prev

            self.size -= 1
            return node_to_remove

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next

    def __str__(self):
        current_node = self.head
        return_str = f's{self.size} h{self.head} t{self.tail}:'
        while current_node is not None:
            return_str += f' > {str(current_node.data)}'
            current_node = current_node.next

        return return_str
