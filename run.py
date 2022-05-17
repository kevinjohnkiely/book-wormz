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

# new_sheet = SHEET.add_worksheet(title="testing", rows="100", cols="20")

# worksheet_objs = SHEET.worksheets()
# worksheets_list = []
# for worksheet in worksheet_objs:
#     worksheets_list.append(worksheet.title)
# print(worksheets_list)

# test = SHEET.worksheet('kevin1234')

# data = test.get_all_values()

# print(data)

print("WELCOME TO BOOKWORMZ! Add, manage and review your favourite books :)")

while True:
    user_input = input("Press 'L' to login, or 'R' to register:\n")
    if(user_input == 'L'):
        print("login function")
        break
    elif (user_input == 'R'):
        print("register function")
        break
    else:
        print("Invalid choice, please go again!")

