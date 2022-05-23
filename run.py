import gspread
from google.oauth2.service_account import Credentials
import datetime
import pyfiglet
from tabulate import tabulate

# Setup the connection and authorizations between application and google sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BookWormz')

ascii_banner = pyfiglet.figlet_format(">>> BOOK-WORMZ <<<")
print(ascii_banner)


def user_login():
    """
    This function takes the users input details, and checks against
    any empty values submitted. It then forwards the username and password
    to the authenticate_user function.
    """
    while True:
        user_name = validate_login_input("username")
        user_pass = validate_login_input("password")

        if authenticate_user(user_name, user_pass):
            print(f"You are logged in as user {user_name}!")
            user_dashboard(user_name)
            break

        print("Your details are incorrect, please try again!")


def user_register():
    """
    This function takes the users input details, and enters their details
    into a dedicated sheet for that user in the google sheet.
    """
    user_name = validate_signup_input("username")
    user_pass = validate_signup_input("password")

    while True:
        user_pass_confirm = input("Please confirm your password:\n")

        if user_pass_confirm == user_pass:
            print("Passwords match!!")
            break
        if user_pass_confirm != user_pass:
            print("Passwords do not match! Try again")

    print(f"You are signed up & logged in as user {user_name}!")

    # Write valid user details to new sheet and populate rows
    SHEET.add_worksheet(title=user_name, rows="100", cols="20")
    user_sheet = SHEET.worksheet(user_name)
    user_sheet.append_row(["Username", "Password", "Date Joined"])
    user_sheet.format('A1:C1', {'textFormat': {'bold': True}})
    user_sheet.append_row(
        [user_name, user_pass, str(datetime.datetime.now().date())])
    user_sheet.append_row([" ", " ", " ", " "])
    user_sheet.append_row(["Book ID", "Book Title", "Author", "Category"])
    user_sheet.format('A3:D3', {'textFormat': {'bold': True}})

    user_dashboard(user_name)


def user_dashboard(user_name):
    """
    This function serves as the user dashboard for the user once they are
    logged in. The user can decide to add/update/delete a book, view their
    books or log out from system.
    """
    print(f"Welcome to your User Dashboard, {user_name}!\n")
    # Get all user data for this username
    user_data = SHEET.worksheet(user_name)
    user_book_data = user_data.get_all_values()[3:]

    while True:
        user_input = input(
            "Press 'B' to view your books, 'A' to add a book, or 'X' to logout:\n")
        if user_input == 'X':
            print("You are now logged out")
            init()
            break
        if user_input == 'B':
            view_all_books(user_data, user_name, user_book_data)
            break
        if user_input == 'A':
            add_book(user_name, user_data, user_book_data)
            break
        print("Invalid choice, please type B, A or X!")


def view_all_books(user_data, user_name, user_book_data):
    """
    This function displays all the users books if they request, or a
    message telling user that they have no books added yet. From this
    list the user can select a book for further actions such as edit or delete.
    """
    if user_book_data:
        print(tabulate(user_book_data))
        while True:
            print("Need to change book details?")
            user_input = input("Press E to edit, D to delete, or R to return to dashboard\n")

            if user_input == 'R':
                user_dashboard(user_name)
            if user_input == 'E':
                edit_book()
                break
            if user_input == 'D':
                delete_book(user_data, user_book_data)
                break
            print("Invalid choice, please try again")
    else:
        print("You have no books added yet!")
        user_dashboard(user_name)


def add_book(user_name, user_data, user_book_data):
    """
    This function takes the user input and creates a new record \
         in the sheet relating to the users chosen book details
    """
    while True:
        print("Please add book details in the following format \
        of comma separated values")
        print("Book Title,Author,Category")
        print("Example: The 2 Towers,JRR Tolkien,Fantasy")

        book_input_string = input("Enter book details:\n")

        book_data = book_input_string.split(",")

        if validate_book_data(book_data):
            print("Data is in correct format!")
            break

    # Assign book ID
    new_book_id = assign_book_id(user_book_data)
    book_data.insert(0, new_book_id)

    user_data.append_row(book_data)
    
    user_dashboard(user_name)


def edit_book():
    print("In edit book function")
    

def delete_book(user_data, user_book_data):
    """
    This function takes an ID relating to a book selected by the user and
    deletes that record from the google sheet.
    """
    while True:
        user_input_id = int(input("Please select book ID from above list:\n"))
        if check_book_id(user_book_data, user_input_id):
            print(f"Book id to be deleted is {user_input_id}")
            # delete the book from data list in memory
            new_list_of_books = []
            for book in user_book_data:
                if int(book[0]) != user_input_id:
                    new_list_of_books.append(book)
            print(new_list_of_books)
            # Clear book records in sheet
            for i in range(4, len(user_book_data) + 4):
                user_data.update(f'A{i}:D{i}', [[" ", " ", " ", " "]])
            # Write new list back to sheet
            for book in new_list_of_books:
                user_data.append_row(book)
            break
        print("That book ID does not exist! Please try another")
    

# UTILITY FUNCTIONS


def validate_login_input(input_name):
    """
    This function validates the user input for the login functionality, so that
    the user cannot submit empty values
    """
    while True:
        user_input_field = input(f'Please enter your {input_name}:\n')

        if len(user_input_field) > 0:
            return user_input_field
            # break
        if len(user_input_field) == 0:
            print(f"{input_name} cannot be empty, try again!")


def validate_signup_input(input_name):
    """
    This function validates the user input for the signup functionality, so that
    the user cannot submit empty values
    """
    while True:
        user_input_field = input(f'Please choose a {input_name} (4-10 characters):\n')
        user_name_exists = check_username(user_input_field)

        if len(user_input_field) > 3 and len(user_input_field) < 11 and not user_name_exists:
            print(f"Your {input_name} {user_input_field} is valid!")
            return user_input_field
        if user_name_exists:
            print(f"{input_name} already exists! Please pick another")
        if len(user_input_field) > 0 and len(user_input_field) < 4:
            print(f"{input_name} is too short! Try again")
        if len(user_input_field) > 10:
            print(f"{input_name} is too long! Try again")
        if len(user_input_field) == 0:
            print(f"{input_name} cannot be empty, try again!")


def authenticate_user(user_name, user_pass):
    """
    This function takes the user details and checks them against those stored
    in the google sheet for valid values.
    """
    # get list of current usernames from sheet
    worksheet_objs = SHEET.worksheets()
    username_list = []
    for worksheet in worksheet_objs:
        username_list.append(worksheet.title)

    if user_name in username_list:
        if check_password(user_name, user_pass):
            return True
    else:
        return False


def check_password(user_name, user_pass):
    """
    Utility function that checks user password in sheet
    """
    user_sheet = SHEET.worksheet(user_name)
    user_data = user_sheet.get_all_values()
    user_data_row = user_data[1]
    user_password = user_data_row[1]
    if user_pass == user_password:
        return True
    return False


def check_username(user_name):
    """
    Utility function that checks if chosen username already exists in sheet
    """
    # get list of current usernames from sheet
    worksheet_objs = SHEET.worksheets()
    username_list = []
    for worksheet in worksheet_objs:
        username_list.append(worksheet.title)

    if user_name in username_list:
        return True
    return False


def validate_book_data(book_data):
    """
    This utility function takes the user input of comma separated values
    and determines if it is in the correct format for sending to the sheet
    """
    print("In validate book data function")
    print(book_data)

    try:
        if len(book_data) != 3:
            raise ValueError(
                f"3 values required (Book title, author, category), \
                     but you provided {len(book_data)}"
            )
    except ValueError as err:
        print(f"Invalid data entered: {err}, please try again.\n")
        return False

    return True


def check_book_id(data, book_id):
    """
    This utility function checks that the book ID that the user selected exists
    in their lists of books.
    """
    book_ids = []
    for book in data:
        book_ids.append(int(book[0]))

    if book_id in book_ids:
        print("the ids match")
        return True
    return False


def assign_book_id(user_book_data):
    """
    This function either sets new ID of 1 for a new book if no books are present,
    or increments the ID of the last book in the users records, to ensure there are
    no clashes of ID numbers
    """
    if not user_book_data:
        return 1
    else:
        return int(user_book_data[-1][0]) + 1


def init():
    """
    This function starts the application and asks the user for their
    first input
    """
    print("WELCOME TO BOOKWORMZ! Add, manage and review your favourite books :)")

    while True:
        user_input = input(
            "Press 'L' to login, or 'R' to register, or 'X' to quit:\n")
        if user_input == 'L':
            user_login()
            break
        if user_input == 'R':
            user_register()
            break
        if user_input == 'X':
            print("GOODBYE")
            quit()
        else:
            print("Invalid choice, please type L, R or X!")


init()
