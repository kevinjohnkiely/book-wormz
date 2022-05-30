# Book-Wormz - Project 3

BookWormz is a Python terminal application which runs on the Code Institute mock terminal on Heroku.

It is a system where a user can signup, login, and add their favourite books. The user can also perform full CRUD (Create, Read, Update, Delete) operations on these books as they wish.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/screengrab.jpg">

## User Flow Diagram

The following diagram gives an outline of the users flow of actions through the application and the different choices of actions that can be undertaken.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/UserFlowDiagram.png">

## Backend Data Storage

The application stores user and book data in the backend using a Google Spreadsheet, with the necessary packages and code included to link Python with the APIs needed. A user has all their information stored on a dedicated sheet within the spreadsheet, this new sheet being added and partially pre-populated on user signup.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/sheet.jpg">

## Coding and Architecture Approach

For this application, I undertook a procedural approach to building the architecture. All functionality is broken down into functions, with the necessary variables and/or lists of data being passed from function to function. In some cases, some functionality was outsourced into utility functions, a list of which can be seen at the bottom half of the Python file. Where possible, some repeating code was also outsourced into separate smaller functions, to best adhere to the DRY principles of software engineering (Don't Repeat Yourself)

## Application User Journeys

The following are a list of the user journeys that can be taken through the application:

### Create New Account

On loading the application, the intro screen provides the user with 3 options, and they choose R to register a new account, X can be typed to quit application.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/introScreen.jpg">

The user is then prompted to choose a username and password. There are a number of validation rules that come into play at this point:
+ Username/Password must be between 4 and 10 characters long
+ The user is asked to confirm password and this must match the initally entered password
+ Username must not already exist in the database (spreadsheet)

Once all this is validated, the user is automatically logged in and forwarded to the User Dashboard screen, where they can make further choices, or press X to logout.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/dashScreen.jpg">

### Login to Account

In the main welcome screen, the user presses L to login.

This process is almost identical to the above Create New Account user journey, the slight difference being the user is not asked to confirm password, or there is no check to see if username exists, as these credentials are already created and stored in database.

### Add New Book

In the User Dashboard screen, the user chooses A to add a new book to their records. The user is prompted to enter 3 fields, the Book title, author and category. The user is then asked if they have already read the book, or would just like to add it to their "wish list". If they choose Y, then they are also asked to rate the book out of 5. If they haven't read the book yet, a rating of 0 is automatially applied and they are not asked to enter this rating. User is returned to dashboard once the book details have been validated and submitted.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/addScreen.jpg">

### View All Books

In order to edit or delete book details, the user must first view all book details in a list, so that they can see what ID number the book is, and then choose this book for modifications. In the User Dashboard, the user types B to view a list of all their books.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/viewScreen.jpg">

### Update Book Details

The updating of book details is limited to the user choosing to update their rating of the book, or whether they would like to move the book from their "read list". In the main dashboard, the user must choose to first view all books. The user then types E to enter edit mode, and the ID of the book from the list. If the ID does not exist, they will be prompted to start edit process again. Once the ID exists, the user is asked to update details, and is forwarded back to previous menu once this completes successfully.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/editScreen.jpg">

### Delete Book

To delete a book, the user begins from the same screen as the editing functionality, whereby they first choose B to view all books from the main dashboard, and then D to delete a book once they can see all book IDs in the list. The user chooses a book ID, and similar to the edit feature, will return an error message and restart the process if the ID does not exist in the backend. Once the book has been deleted, the user is returned to the dashboard where they can once again view their books, with the chosen book now deleted.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/deleteScreen.jpg">

## Testing

I tested the application thoroughly through each user journey, ensuring that at no point the system crashes due to unexpected input. In several parts of the application, loops are used when concerned with accepting user input, to ensure that the user is repeatedly asked to enter the correctly formatted information, and program flow will only continue until the data is valid.

I carried out this testing both on the Gitpod development environment, and also on the Heroku equivalent after successful deployment.

I ran the Python source code through the online Pep8 Validator (http://pep8online.com/) and other than some warnings about lines exceeding the recommended 79 character lengths, no erros were reported.

## Bugs, Issues and Errors

There were a number of bugs which appeared during development of this application, all of which arose from the same formatting issue.

To write the data from the application to the Google Sheet, I used the Gspread library to do so but however could not find any method within this package that would update or delete a spreadsheet row in the format that I wished. Thus, I decided to solve this by fetching all the records of the sheet into memory, wipe the spreadsheet book records, edit/delete the chosen record and then re-write the new data back into the spreadsheet. This eventually proved successful, but a formatting issue cropped up as seen in the following screenshot:

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/bugs.jpg">

The data record for the "Read list" column should be a boolean value as that is how it was intially formatted, however reading the data back from the spreadsheet it returned as either 'TRUE' or 'FALSE', a string value. Through further investigation I discovered that any non-empty string evaluates as True, thus all the records switched to true values when some should have been false. I wrote a small piece of code to rectify this and solve the bug.

## Deployment

The following were the steps undertaken to deploy the project to Heroku:

+ In the gitpod terminal, run 'pip3 freeze > requirements.txt' to install dependancies such as gspread and google auth into the Heroku platform.
+ After login to Heroku account, create a new app.
+ Navigate to settings tab, and go to Reveal Config Vars button
+ Add 2 new Config vars, copy and paste the contents of Creds.json for the CREDS key, and enter value of 8000 for the PORT key.
+ Click "Add Buildpack" and add Python and Node.js in that order
+ Navigate to Deploy tab, choose Github and confirm connection to github account
+ Click Deploy Branch, and application is now deployed.


## Credits