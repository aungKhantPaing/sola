from datetime import datetime
from getpass import getpass
from database import DatabaseManager
from models.borrowed_item_list import BorrowedItemList
from models.library_tree.library_trees import LibraryTrees
from models.users.admin import Admin
from models.users.borrower import Borrower
from models.borrower_list import BorrowerList


def login(borrower_list, admin=Admin('admin', 'passw0rd', 'John', 'Doe')):
    print("Welcome to the Library System")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if username == admin.username and admin.verify_password(password):
        print("Admin login successful!")
        return admin

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


def search_item(library_trees: LibraryTrees, attribute, value):
    if attribute not in library_trees.library_trees:
        print("Invalid attribute. Please try again.")
        return None
    else:
        return library_trees.search(attribute, value)


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


def add_borrowable_item(db: DatabaseManager, library_trees: LibraryTrees):
    print("1. Book")
    print("2. Audio Book")
    print("3. Periodical")
    borrowable_type = input("Enter the type of borrowable you want to add: ")
    title = input("Enter title: ")
    category = input("Enter category: ")
    language = input("Enter language: ")
    authors = input("Enter authors (separate with comma): ")
    year_published = int(input("Enter year published: "))
    if borrowable_type == '1':
        isbn = input("Enter ISBN: ")
        borrowable = db.insert_book(title, category, language, authors, year_published, isbn)
    elif borrowable_type == '2':
        isbn = input("Enter ISBN: ")
        audio_format = input("Enter audio format: ")
        borrowable = db.insert_audio_book(title, category, language, authors, year_published, isbn, audio_format)
    elif borrowable_type == '3':
        borrowable = db.insert_periodical(title, category, language, authors, year_published)
    else:
        print("Invalid borrowable type. Please try again.")
        return
    library_trees.insert(borrowable)
    print(f"Successfully added {borrowable}")


def remove_borrowable_item(db: DatabaseManager, library_trees: LibraryTrees):
    borrowable_id = input("Enter borrowable ID: ")
    borrowable = db.get_borrowable_by_id(borrowable_id)
    if borrowable:
        db.delete_borrowable(borrowable_id)
        library_trees.rebuild_library_tree(db.get_borrowables())
        print(f"Successfully removed {borrowable}")
    else:
        print("Borrowable not found. Please try again.")


def add_borrower(db: DatabaseManager, borrower_list: BorrowerList):
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    borrower = db.insert_borrower(username, password, first_name, last_name)
    borrower_list.append(borrower)
    print(f"Successfully added {borrower}")


def remove_borrower(db: DatabaseManager, borrower_list: BorrowerList):
    account_number = input("Enter account number: ")
    borrower = borrower_list.search_by_account_number(account_number)
    if borrower:
        db.delete_borrower(borrower.account_number)
        borrower_list.remove_by_account_number(borrower.account_number)
        print(f"Successfully removed {borrower}")
    else:
        print("Borrower not found. Please try again.")


def admin_interface(user: Admin, library_trees, borrowed_items, borrower_list, db: DatabaseManager, borrowables):
    while True:
        print()
        print("--- Admin Main Menu ---")
        print("1. Search for items")
        print("2. View borrowable items")
        print("3. Add or remove items")
        print("4. Add or remove borrowers")
        print("5. Locate borrowers with unpaid fines")
        print("6. List items borrowed by each borrower")
        print("7. List all borrowers")  # New option
        print("8. Exit")
        option = input("Please enter your choice: ")
        if option == '1':
            attribute = input("Enter attribute to search (title, category, language, year_published, author): ")
            value = input("Enter value to search: ")
            items = search_item(library_trees, attribute, value)
            if items:
                print(f"Found {len(items)} items with {attribute}: {value}")
                for i, item in enumerate(items, start=1):
                    print(f"{i}. {item}")
            else:
                print("No items found with that attribute and value.")
        elif option == '2':
            view_borrowables_paginated(borrowables)
        elif option == '3':
            print("1. Add item")
            print("2. Remove item")
            sub_option = input("Please enter your choice: ")
            if sub_option == '1':
                add_borrowable_item(db, library_trees)
            elif sub_option == '2':
                remove_borrowable_item(db, library_trees)
        elif option == '4':
            print("1. Add borrower")
            print("2. Remove borrower")
            sub_option = input("Please enter your choice: ")
            if sub_option == '1':
                add_borrower(db, borrower_list)
            elif sub_option == '2':
                remove_borrower(db, borrower_list)
        elif option == '5':
            borrowers_with_unpaid_fines = [borrower for borrower in borrower_list if
                                           borrower.has_unpaid_fines(borrowed_items)]
            if borrowers_with_unpaid_fines:
                print(f"Found {len(borrowers_with_unpaid_fines)} borrowers with unpaid fines.")
                for i, borrower in enumerate(borrowers_with_unpaid_fines, start=1):
                    print(f"{i}. {borrower.username} (${borrower.get_total_fines(borrowed_items)})")
            else:
                print("No borrowers with unpaid fines.")
        elif option == '6':
            for borrower in borrower_list:
                borrowed_items_by_borrower = borrowed_items.search_unreturned_items(borrower.account_number)
                print(f"{borrower.username} has borrowed {len(borrowed_items_by_borrower)} items.")
                for i, item in enumerate(borrowed_items_by_borrower, start=1):
                    print(f"    {i}. {item}")
        elif option == '7':
            for i, borrower in enumerate(borrower_list, start=1):
                print(f"{i}. {borrower}")
        elif option == '8':
            break
        else:
            print("Invalid option. Please try again.")


def borrower_interface(user: Borrower, library_trees, borrowed_items, db: DatabaseManager, borrowables):
    while True:
        print()
        print("--- Borrower Main Menu ---")
        print("1. View borrowable items")
        print("2. Search and borrow item")
        print("3. View borrowed items")
        print("4. View and pay fines")
        print("6. Exit")
        option = input("Please enter your choice: ")
        if option == '1':
            view_borrowables_paginated(borrowables)
        elif option == '2':
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
        elif option == '5':
            break
        else:
            print("Invalid option. Please try again.")


def main():
    db = DatabaseManager("library.sqlite")

    # admin = Admin('admin', 'passw0rd', 'John', 'Doe')
    borrowers = db.get_borrowers()
    borrower_list = BorrowerList()
    for borrower in borrowers:
        borrower_list.append(borrower)

    borrowables = db.get_borrowables()
    library_trees = LibraryTrees(borrowables)

    borrowed_items = BorrowedItemList()
    for borrowed_item in db.get_borrowed_items():
        borrowed_items.append(borrowed_item)

    user = None
    while not user:
        user = login(borrower_list)

    if isinstance(user, Admin):
        admin_interface(user, library_trees, borrowed_items, borrower_list, db, borrowables)
    elif isinstance(user, Borrower):
        borrower_interface(user, library_trees, borrowed_items, db, borrowables)
    else:
        print("Invalid user type. Please try again.")


if __name__ == "__main__":
    main()
