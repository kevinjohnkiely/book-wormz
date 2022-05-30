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

## Login to Account

In the main welcome screen, the user presses L to login.

This process is almost identical to the above Create New Account user journey, the slight difference being the user is not asked to confirm password, or there is no check to see if username exists, as these credentials are already created and stored in database.

## Add New Book

In the User Dashboard screen, the user chooses A to add a new book to their records. The user is prompted to enter 3 fields, the Book title, author and category. The user is then asked if they have already read the book, or would just like to add it to their "wish list". If they choose Y, then they are also asked to rate the book out of 5. If they haven't read the book yet, a rating of 0 is automatially applied and they are not asked to enter this rating. User is returned to dashboard once the book details have been validated and submitted.

<img src="https://github.com/kevinjohnkiely/book-wormz/blob/main/wireframesScreenshots/addScreen.jpg">