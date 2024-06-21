from models.library_tree.library_tree import LibraryTree
from models.library_tree.multi_key_library_tree import MultiKeyLibraryTree


class LibraryTrees:
    def __init__(self, borrowables):
        self.library_trees = self.create_library_trees(borrowables)

    def search(self, key, value):
        return self.library_trees[key].search(value)

    def insert(self, borrowable):
        for key, library_tree in self.library_trees.items():
            library_tree.insert(borrowable)

    def rebuild_library_tree(self, borrowables):
        self.library_trees = self.create_library_trees(borrowables)

    @staticmethod
    def create_library_trees(borrowables):
        library_trees = {
            'title': LibraryTree(lambda item: item.title),
            'category': LibraryTree(lambda item: item.category),
            'language': LibraryTree(lambda item: item.language),
            'year_published': LibraryTree(lambda item: str(item.year_published)),
            'author': MultiKeyLibraryTree(lambda item: item.authors)
        }
        for borrowable in borrowables:
            library_trees['title'].insert(borrowable)
            library_trees['category'].insert(borrowable)
            library_trees['language'].insert(borrowable)
            library_trees['year_published'].insert(borrowable)
            library_trees['author'].insert(borrowable)
        return library_trees
