import gspread
from google.oauth2.service_account import Credentials
import datetime
import pyfiglet

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

current_logged_in_user = None

# new_sheet = SHEET.add_worksheet(title="testing", rows="100", cols="20")


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


def user_login():
    """
    This function takes the users input details, and checks against
    any empty values submitted. It then forwards the username and password
    to the authenticate_user function.
    """
    while True:
        while True:
            user_name = input('Please enter your username:\n')

            if len(user_name) > 0:
                break
            if len(user_name) == 0:
                print("Username cannot be empty, try again!")

        while True:
            user_pass = input('Please enter your password:\n')

            if len(user_pass) > 0:
                break
            if len(user_pass) == 0:
                print("Password cannot be empty, try again!")

        if authenticate_user(user_name, user_pass):
            current_logged_in_user = user_name
            print(f"You are logged in as user {current_logged_in_user}!")
            break

        print("Your details are incorrect, please try again!")


def user_register():
    """
    This function takes the users input details, and enters their details
    into a dedicated sheet for that user in the google sheet.
    """
    while True:
        user_name = input('Please choose a username (4-10 characters):\n')
        user_name_exists = check_username(user_name)

        if len(user_name) > 3 and len(user_name) < 11 and not user_name_exists:
            print(f"Your username {user_name} is valid!")
            break
        if user_name_exists:
            print("Username already exists! Please pick another")
        if len(user_name) > 0 and len(user_name) < 4:
            print("Username is too short! Try again")
        if len(user_name) > 10:
            print("Username is too long! Try again")
        if len(user_name) == 0:
            print("Username cannot be empty, try again!")

    while True:
        user_pass = input('Please choose a password (4-10 characters):\n')

        if len(user_pass) > 3 and len(user_pass) < 11:
            print(f"Your password {user_pass} is valid!")
            break
        if len(user_pass) > 0 and len(user_pass) < 4:
            print("Password is too short! Try again")
        if len(user_pass) > 10:
            print("Password is too long! Try again")
        if len(user_pass) == 0:
            print("Password cannot be empty, try again!")
           
    while True:
        user_pass_confirm = input("Please confirm your password:\n")

        if user_pass_confirm == user_pass:
            print("Passwords match!!")
            break
        if user_pass_confirm != user_pass:
            print("Passwords do not match! Try again")

    print(f"your details are {user_name} and {user_pass}")
    # Write valid user detais to new sheet and populate rows
    SHEET.add_worksheet(title=user_name, rows="100", cols="20")
    user_sheet = SHEET.worksheet(user_name)
    user_sheet.append_row(["Username", "Password", "Date Joined"])
    user_sheet.append_row([user_name, user_pass, str(datetime.datetime.now().date())])


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
