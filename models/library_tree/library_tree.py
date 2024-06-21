from models.library_tree.node import Node


class LibraryTree:
    def __init__(self, get_key):
        self.root = None
        self._get_key = get_key

    def insert(self, item):
        key = self._get_key(item)
        # print(f"Inserting item with key {key}")
        if not self.root:
            self.root = Node(key, item)
        else:
            self._insert(self.root, key, item)

    # def _get_key(self, item):
    #     return getattr(item, self.attribute)

    def _insert(self, node, key, item):
        # print(f"Inserting item with key {key} at node with key {node.key}")
        if key < node.key:
            if node.left is None:
                node.left = Node(key, item)
            else:
                self._insert(node.left, key, item)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key, item)
            else:
                self._insert(node.right, key, item)
        else:
            node.items.append(item)

    def search(self, value):
        # print(f"Searching for item with key {value}")
        if self.root:
            return self._search(self.root, value)
        else:
            return None

    def _search(self, node, value):
        # print(f"Checking node with key {node.key}")
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

    def get_all_nodes(self):
        return self._get_all_nodes(self.root)

    def _get_all_nodes(self, node):
        if not node:
            return []
        return self._get_all_nodes(node.left) + [node] + self._get_all_nodes(node.right)

    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                node.key = self._min_value(node.right)
                node.right = self._delete_node(node.right, node.key)
        return node

    @staticmethod
    def _min_value(node):
        current = node
        while current.left:
            current = current.left
        return current.key

    def __str__(self):
        return self._in_order_traversal(self.root, "")

# class MultiSearchTree:
#     def __init__(self, attributes):
#         self.trees = {attribute: BinarySearchTree(attribute) for attribute in attributes}
#
#     def insert(self, item):
#         for tree in self.trees.values():
#             tree.insert(item)
#
#     def search(self, attribute, value):
#         if attribute in self.trees:
#             return self.trees[attribute].search(value)
#         else:
#             return None
