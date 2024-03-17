# SpendWise - Expense Tracker
#### Video Demo: https://youtu.be/fZyci5fBFE4
#### Description:

SpendWise is a web application that is used to monitor and manage personal finance and expenses. 
Tools and programming languages used
- Visual Studio Code
- Python 
- Flask Framework
- CSS
- HTML
- Javascript
- Bootstrap
- SQL

Features of SpendWise (For registered users)
- Expense Recording
- Categorization
- Budgeting
- Dashboard (Overview of expense and budget)

Features of SpendWise (For both registered and non-registered users)
- Register
- Login

Users can record details of their expenses, including category of expense(eg. food & groceries, transportation etc), amount, date and description (if applicable) of expense.

The expenses can be categorized into different categories to organize and analyze spending patterns. Common categories are pre-added -
(Food & Groceries, Housing, Transportation, Healthcare, Entertainment, Education, Debt Payments, Savings & Investments, Travel, Utilities, Clothing & Accessories, Miscellaneous)

Budgeting is a feature that allows users to set budgets for different expense categories to set spending limits and track their progress. 

Dashboard on the home page is a visual representation of user expenses and budgets

Users are required to register and login before they can access the logging features of SpendWise.

A SQL database expense.db is used to log user details, expenses, budgets and categories of expenses

.schema of expense.db

CREATE TABLE users (
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           password_hash TEXT NOT NULL);

CREATE TABLE category (
           id INTEGER PRIMARY KEY, 
           category_name TEXT NOT NULL);

CREATE TABLE expense (
           id INTEGER PRIMARY KEY,
           user_id INTEGER NOT NULL,
           category_id INTEGER NOT NULL, 
           amount REAL NOT NULL, 
           date DATETIME NOT NULL,
           description TEXT, 
           FOREIGN KEY (user_id) REFERENCES users(id));

CREATE TABLE budget (
           id INTEGER PRIMARY KEY,
           category_id INTEGER NOT NULL,
           user_id INTEGER NOT NULL,
           amount REAL NOT NULL,
           start DATE NOT NULL,
           end DATE NOT NULL,
           FOREIGN KEY (category_id) REFERENCES category(id), 
           FOREIGN KEY (user_id) REFERENCES users(id));


Files

/templates/layout.html

layout.html is a template that defines the overall structure and layout of the web application, it contains the static elements that are common across all pages (scripts in head tag, navigation menu in header of body tag etc).
All other html files in the templates folder extends layout.html.

/templates/index.html

index.html is a dashboard that shows the current session user an overview of his/her expenses and active budgets. It contains 2 buttons expense and budget that user can click on to swap the views. The expenses overview contains a visual representation of user expenses in a doughnut chart, a summary of expenses, and also timeframe buttons that allows the user to sort his/her expenses via week, month, 3 months, year and custom dates. The charts are created and updated via AJAX. On the other hand, the budget view shows the user's active budgets. It contains a visual representation of user budgets and expenses within the period of budget in a bar chart. 

/templates.expense.html

expense.html contains a table that shows the current session user's logged expenses in the form of a table. The user can add new expenses, edit and delete existing expenses on the page, these operations are performed via a form POST request. The user inputs are both validated on the client side and server side.

/templates/budget.html

Similar to expense.html, budget.html contains a table that shows the current session user's created budgets. The usre can create new budgets, edit and delete existing budgets on the page, these operations are performed via a form POST request. The user inputs are both validated on the client side and server side.

/templates/login.html

login.html contains a form that allows users to log into the web application. Form inputs are both validated on the client side and server side. Client side validation checks if any input fields are left blank, and the server side validation checks if any inputs are blank, then the database if the username and hash of user password matches the entry in the users table. If it matches, user is logged in and can access the features of SpendWise for registered users, else user is redirected back to the login page with a error message.

/templates/register.html

register.html contains a form that allows new users to register. Form inputs are both validated on the client side and server side. Client side validation checks for any blank input fields, and servier side validation checks for blank inputs, and then checks the database if the username is already created/used by another user. If passed check, new user is added to the database, else user is redirected back to register page with error message.

app.py

app.py is the main python file that contains the configuration of the Flask application. It contains the import dependencies, flask application creation, define routes used, and handles requests.

db.py

db.py contains the configuration for expense.db database.

expense.db

database file for the web application.

helpers.py

helpers.py contains functions used.

/static

the static folder contains static files (images, javascript files and css file) that are used within the web application.