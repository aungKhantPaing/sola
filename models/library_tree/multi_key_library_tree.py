from models.library_tree.library_tree import LibraryTree
from models.library_tree.node import Node


class MultiKeyLibraryTree(LibraryTree):
    def insert(self, item):
        keys = self._get_key(item)
        print(f"Inserting item with keys {keys}")
        if not self.root:
            self.root = Node(keys[0], item)
            for key in keys[1:]:
                self._insert(self.root, key, item)
        else:
            for key in keys:
                self._insert(self.root, key, item)


