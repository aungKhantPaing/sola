from database import DatabaseManager
from models.binary_search_tree import BinarySearchTree


def main():
    print("Hello, World!")
    db = DatabaseManager("library.sqlite")
    borrowables = db.get_borrowables()
    library_tree_title = BinarySearchTree("title")
    # library_tree_year = BinarySearchTree("year_published")
    for borrowable in borrowables:
        library_tree_title.insert(borrowable)
        # library_tree_year.insert(borrowable)

    print(library_tree_title)
    library_tree_title.print_tree()
    # print(library_tree_year)
    print(library_tree_title.search("Becoming"))
    # print(library_tree_year.search(2024))


if __name__ == "__main__":
    main()