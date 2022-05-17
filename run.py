import gspread
from google.oauth2.service_account import Credentials
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

CURRENT_LOGGED_IN_USER = None

# new_sheet = SHEET.add_worksheet(title="testing", rows="100", cols="20")


# test = SHEET.worksheet('kevin1234')

# data = test.get_all_values()

# print(data)


def user_login():
    """
    This function takes the users input details, and checks against
    any empty values submitted. It then forwards the username and password
    to the authenticate_user function.
    """
    while True:
        user_name = input('Please enter your username:\n')

        if len(user_name) > 0:
            break
        elif len(user_name) == 0:
            print("Username cannot be empty, try again!")

    while True:
        user_pass = input('Please enter your password:\n')

        if len(user_pass) > 0:
            break
        elif len(user_pass) == 0:
            print("Password cannot be empty, try again!")

    # print(f'user name is {user_name} and pass is {user_pass}')
    if authenticate_user(user_name, user_pass):
        print("User exists!")


print("WELCOME TO BOOKWORMZ! Add, manage and review your favourite books :)")

while True:
    user_input = input(
        "Press 'L' to login, or 'R' to register, or 'X' to quit program:\n")
    if user_input == 'L':
        user_login()
        break
    elif user_input == 'R':
        print("register function")
        break
    elif user_input == 'X':
        print("GOODBYE")
        quit()
    else:
        print("Invalid choice, please type L, R or X!")
