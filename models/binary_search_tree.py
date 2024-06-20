from typing import Generic, TypeVar

T = TypeVar('T')


class Node:
    def __init__(self, key, item):
        self.key = key
        self.items = [item]
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, attribute):
        self.root = None
        self.attribute = attribute

    def insert(self, item):
        print(f"Inserting item with key {self._get_key(item)}")
        if not self.root:
            self.root = Node(self._get_key(item), item, )
        else:
            self._insert(self.root, item)

    def _get_key(self, item):
        return getattr(item, self.attribute)

    def _insert(self, node, item):
        key = self._get_key(item)
        print(f"Inserting item with key {key} at node with key {node.key}")
        if key < node.key:
            if node.left is None:
                node.left = Node(key, item)
            else:
                self._insert(node.left, item)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, item)
            else:
                self._insert(node.right, item)
        else:
            node.items.append(item)

    def search(self, value):
        print(f"Searching for item with key {value}")
        if self.root:
            return self._search(self.root, value)
        else:
            return None

    def _search(self, node, value):
        print(f"Checking node with key {node.key}")
        if value < node.key and node.left:
            return self._search(node.left, value)
        elif value > node.key and node.right:
            return self._search(node.right, value)
        elif value == node.key:
            return node.items
        else:
            return None

    def _in_order_traversal(self, node, result):
        if node:
            result = self._in_order_traversal(node.left, result)
            result += str(node.key) + ", "
            result = self._in_order_traversal(node.right, result)
        return result

    def print_tree(self, node=None, level=0):
        if not node:
            node = self.root
        if node.right:
            self.print_tree(node.right, level + 1)
        print('    ' * level + '->', node.key)
        if node.left:
            self.print_tree(node.left, level + 1)

    def __str__(self):
        return self._in_order_traversal(self.root, "")


class MultiSearchTree:
    def __init__(self, attributes):
        self.trees = {attribute: BinarySearchTree(attribute) for attribute in attributes}

    def insert(self, item):
        for tree in self.trees.values():
            tree.insert(item)

    def search(self, attribute, value):
        if attribute in self.trees:
            return self.trees[attribute].search(value)
        else:
            return None
