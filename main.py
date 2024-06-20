from getpass import getpass
from database import DatabaseManager
from models.library_tree.library_tree import LibraryTree
from models.library_tree.multi_key_library_tree import MultiKeyLibraryTree
from models.users.admin import Admin
from models.users.borrower import Borrower
from models.borrower_list import BorrowerList


def login(borrower_list):
    print("Welcome to the Library System")
    username = input("Please enter your username: ")
    password = getpass("Please enter your password: ")

    user = borrower_list.search(username)
    if user and user.verify_password(password):
        print("Login successful!")
        return user
    else:
        print("Invalid username or password. Please try again.")
        return None


def view_borrowables(library_tree_title):
    print("Borrowable items:")
    library_tree_title.print_tree()


def borrow_item(user, library_tree_title):
    title = input("Enter the title of the item you want to borrow: ")
    item = library_tree_title.search(title)
    if item:
        user.rent_item(item)
        print(f"You have successfully borrowed {title}")
    else:
        print("Item not found. Please try again.")


def paginate(items, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]


def view_borrowables_paginated(library_tree_title, page, page_size):
    items = library_tree_title.items  # Assuming that the tree has an 'items' property that returns a list of all items
    items_on_page = paginate(items, page, page_size)
    for item in items_on_page:
        print(item.title)  # Assuming that the item has a 'title' property


def view_borrowed_items(user):
    print("Borrowed items:")
    for item in user.rented_items:
        print(item.title)  # Assuming that the item has a 'title' property


def search_borrowables_by_title(library_tree_title, title):
    items = library_tree_title.search(title)
    if items:
        print(f"Found items with title: {title}")
        for item in items:
            print(item)  # Assuming that the item has a 'title' property
    else:
        print("No items found with that title.")


def search_borrowables_by_year(library_tree_year, year):
    items = library_tree_year.search(year)
    if items:
        print(f"Found items from that year: {year} ")
        for item in items:
            print(item)  # Assuming that the item has a 'title' property
    else:
        print("No items found from that year.")


def search_borrowables_by_author(library_tree_author, author):
    items = library_tree_author.search(author)
    if items:
        print(f"Found items by author: {author}")
        for item in items:
            print(item)  # Assuming that the item has a 'title' property
    else:
        print("No items found by that author.")


def main():
    db = DatabaseManager("library.sqlite")

    admin = Admin('admin', 'passw0rd', 'John', 'Doe')
    borrowers = db.get_borrowers()
    borrower_list = BorrowerList()
    for borrower in borrowers:
        borrower_list.append(borrower)

    borrowables = db.get_borrowables()
    library_tree_title = LibraryTree(lambda item: item.title)
    library_tree_year = LibraryTree(lambda item: item.year_published)
    library_tree_author = MultiKeyLibraryTree(lambda item: item.authors)
    for borrowable in borrowables:
        library_tree_title.insert(borrowable)
        library_tree_year.insert(borrowable)
        library_tree_author.insert(borrowable)

    user = None
    while not user:
        user = login(borrower_list)

    while True:
        print("1. View borrowable items")
        print("2. Borrow an item")
        print("3. View borrowed items")
        print("4. Search items by title")
        print("5. Search items by year")
        print("6. Search items by author")
        print("7. Exit")
        option = input("Please enter your choice: ")
        if option == '1':
            page = int(input("Enter page number: "))
            page_size = int(input("Enter page size: "))
            view_borrowables_paginated(library_tree_title, page, page_size)
        elif option == '2':
            borrow_item(user, library_tree_title)
        elif option == '3':
            view_borrowed_items(user)
        elif option == '4':
            title = input("Enter title to search: ")
            search_borrowables_by_title(library_tree_title, title)
        elif option == '5':
            year = int(input("Enter year to search: "))
            search_borrowables_by_year(library_tree_year, year)
        elif option == '6':
            author = input("Enter author to search: ")
            search_borrowables_by_author(library_tree_author, author)
        elif option == '7':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
