from datetime import datetime
from getpass import getpass
from database import DatabaseManager
from models.borrowed_item import BorrowedItem
from models.borrowed_item_list import BorrowedItemList
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


def paginate(items, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]


def view_borrowables_paginated(items, page_size=10):
    total_pages = len(items) // page_size + (len(items) % page_size > 0)
    items_on_page = paginate(items, 1, page_size)
    for i, item in enumerate(items_on_page, start=1):
        print(f"{(1 - 1) * page_size + i}. {item}")

    while True:
        print(f"Total pages: {total_pages}")
        page = int(input("Enter page number (or 0 to go back): "))
        if page == 0:
            break
        elif 1 <= page <= total_pages:
            items_on_page = paginate(items, page, page_size)
            for i, item in enumerate(items_on_page, start=1):
                print(f"{(page - 1) * page_size + i}. {item}")
        else:
            print("Invalid page number. Please try again.")


def view_borrowed_items(user, borrowed_items: BorrowedItemList):
    print("Borrowed items:")
    user_borrowed_items = borrowed_items.search_unreturned_items(user.account_number)
    if not user_borrowed_items:
        print("No items borrowed.")
        return
    for i, item in enumerate(user_borrowed_items, start=1):
        print(f"{i}. {item}")


def return_selected_item(user, item, borrowed_items, db: DatabaseManager):
    confirmation = input(f"Do you want to return {item}? (yes/no): ")
    if confirmation.lower() == 'yes':
        item.return_date = datetime.now()
        db.update_borrowed_item(item)
        print(f"You have successfully returned {item.borrowable_id}")
    else:
        print("You chose not to return the item.")


def search_item(library_trees, attribute, value):
    if attribute not in library_trees:
        print("Invalid attribute. Please try again.")
        return None
    else:
        return library_trees[attribute].search(value)


def borrow_selected_item(user, item, borrowed_items, db: DatabaseManager):
    if borrowed_items.is_item_borrowed(item.id):
        print("This item is already borrowed.")
        return
    confirmation = input(f"Do you want to borrow {item.title}? (yes/no): ")
    if confirmation.lower() == 'yes':
        if user.has_reached_borrow_limit(borrowed_items):
            print("You have reached the maximum number of borrowed items.")
            return
        elif user.has_unpaid_fines(borrowed_items):
            print("You have unpaid fines. Please pay your fines first.")
            return
        else:
            borrowed_item = db.insert_borrowed_item(item.id, user.account_number, datetime.now())
            borrowed_items.append(borrowed_item)
            print(f"You have successfully borrowed {item.title}")
    else:
        print("You chose not to borrow the item.")


def main():
    db = DatabaseManager("library.sqlite")

    admin = Admin('admin', 'passw0rd', 'John', 'Doe')
    borrowers = db.get_borrowers()
    borrower_list = BorrowerList()
    for borrower in borrowers:
        borrower_list.append(borrower)

    borrowables = db.get_borrowables()
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

    borrowed_items = BorrowedItemList()
    for borrowed_item in db.get_borrowed_items():
        borrowed_items.append(borrowed_item)

    user = None
    while not user:
        user = login(borrower_list)

    while True:
        print()
        print("1. View borrowable items")
        print("2. Borrow an item")
        print("3. View borrowed items")
        print("4. Search items")
        print("5. View and pay fines")
        print("6. Exit")
        option = input("Please enter your choice: ")
        if option == '1':
            view_borrowables_paginated(borrowables)
        elif option == '2':
            print('WIP')
        elif option == '3':
            user_borrowed_items = borrowed_items.search_unreturned_items(user.account_number)
            if user_borrowed_items:
                print(f"You have {len(user_borrowed_items)} borrowed items.")
                for i, item in enumerate(user_borrowed_items, start=1):
                    print(f"{i}. {item}")
                item_number = int(input("Enter the number of the item you want to return: "))
                selected_item = user_borrowed_items[item_number - 1]
                return_selected_item(user, selected_item, borrowed_items, db)
            else:
                print("You have no borrowed items.")
        elif option == '4':
            attribute = input("Enter attribute to search (title, category, language, year_published, author): ")
            value = input("Enter value to search: ")
            items = search_item(library_trees, attribute, value)
            if items:
                print(f"Found {len(items)} items with {attribute}: {value}")
                for i, item in enumerate(items, start=1):
                    print(f"{i}. {item}")
                item_number = int(input("Enter the number of the item you want to view in detail: "))
                selected_item = items[item_number - 1]
                print(selected_item.get_detail())
                borrow_selected_item(user, selected_item, borrowed_items, db)
            else:
                print("No items found with that attribute and value.")
        elif option == '5':
            unpaid_fines = user.get_unpaid_fines(borrowed_items)
            if unpaid_fines:
                print(f"You have {len(unpaid_fines)} unpaid fines.")
                for i, item in enumerate(unpaid_fines, start=1):
                    print(f"{i}. {item}")
                item_number = int(input("Enter the number of the fine you want to pay: "))
                selected_item = unpaid_fines[item_number - 1]
                selected_item.pay_fine()
                db.update_borrowed_item(selected_item)
                print(f"You have successfully paid the fine for {selected_item.borrowable_id}")
            else:
                print("You have no unpaid fines.")
        elif option == '6':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
