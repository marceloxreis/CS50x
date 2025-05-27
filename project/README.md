# My finance
#### Video Demo:  <[URL](https://youtu.be/9lpXkQbDmhQ) HERE>
#### Description:
Finance Management Web Application
Project Overview
This Finance Management Web Application is designed to assist users in monitoring and managing their personal finances. Built with Python and Flask, the application features a user-friendly interface for tracking expenses, viewing cash balances, and managing transactions by categories. The backend leverages SQLite for efficient data storage and retrieval, while the front end uses Flask templates for dynamic content rendering. Security is a key consideration, with password hashing and session management incorporated to protect user information.
The app includes several core functionalities:
•	User Registration and Authentication: New users can create accounts securely, while existing users can log in and out with hashed password storage and validation.
•	Dashboard Overview: Displays the user’s current cash balance and detailed records of spending categorized by type.
•	Expense Logging: Users can log new expenses, which are then subtracted from their available cash and stored in the database.
•	Cash Balance Editing: Users have the option to update their total cash balance directly.
•	Transaction Management: Users can remove transactions, which automatically updates the available cash amount to reflect the change.
The application is built to be intuitive, yet it provides robust features for managing financial data effectively.

File Descriptions
app.py
This is the primary file of the application, containing all the Flask routes and handling user requests and interactions with the database. Key elements of app.py include:
1.	Session Configuration: Sets up Flask-Session to handle user sessions using the file system, ensuring session data is secure and not stored in cookies.
2.	Routes: Manages the core functionalities:
o	/ (Index Route): Displays the user's current cash balance and a list of expenses categorized appropriately. It queries the user_data table for transaction details and the users table for the cash balance.
o	/login: Handles user login, validating credentials against the database. If successful, it initializes a user session and redirects to the index page. Error messages are shown for incorrect usernames or passwords.
o	/logout: Logs the user out by clearing the session and redirects to the login page.
o	/register: Manages new user registration. It validates form inputs, hashes passwords, checks for existing usernames, and stores new user details in the users table. Upon successful registration, the user is redirected to the login page.
o	/buy: Enables users to add new expenses. It checks the category and amount for validity, ensures the user has enough cash, and updates the database. If the operation succeeds, the cash balance is adjusted, and the transaction is logged in user_data.
o	/edit: Provides a way to update the cash balance directly. Users input a new amount, and the application updates the balance in the users table.
o	/remove: Deletes a specific transaction from user_data, adding the transaction amount back to the cash balance. This route ensures that only authorized users can delete their transactions.
helpers.py
This file contains utility functions used throughout the application:
•	apology: A function that renders custom error messages, displaying apologies for user mistakes or system errors.
•	login_required: A decorator that restricts access to specific routes, making sure only logged-in users can view or interact with certain pages.
•	lookup: A stub function intended for looking up financial data, which could be expanded for integration with financial APIs in the future.
•	usd: A custom filter for formatting numbers as USD currency, ensuring consistent currency display.
finance.db
The SQLite database file that maintains all user and financial information:
•	users: A table storing user details, including id, username, and a hashed password for secure authentication.
•	user_data: A table recording expenses with columns for user_id, category, amount, and a unique transaction id. This setup allows efficient tracking and management of user expenses.
templates/
This directory contains the HTML templates rendered by Flask to create a dynamic user experience:
•	index.html: Displays the user's financial summary, including cash balance and categorized expenses. It provides a clear view of the user's current financial status.
•	login.html: A simple form for users to log in, with validation messages for incorrect inputs.
•	register.html: A form for new user registration, including fields for username, password, and password confirmation, with feedback for validation errors.
•	buy.html: A form for adding expenses, allowing the user to input a category and amount. Data validation ensures that the amount is positive and within the user’s available cash.
•	edit.html: A form for updating the cash balance. The user inputs a new balance, and the application updates it in the database.
•	apology.html: Used to display error messages when something goes wrong, providing a consistent and user-friendly experience.

Design Decisions
Security
Password security is a top priority, achieved through hashing using generate_password_hash and validation with check_password_hash from werkzeug.security. Sessions are managed securely, with the data stored on the file system rather than in browser cookies, adding a layer of protection. Additionally, route access is restricted to authenticated users using the login_required decorator.
User Experience
The application provides a simple and intuitive interface for managing finances. The design choice to allow direct editing of the cash balance simplifies user input but could be enhanced in the future with detailed audit trails or more granular financial tracking. The flash messages and error handling provide immediate feedback, guiding the user through various operations.
Database Structure
The database schema is optimized for quick and efficient lookups, with separate tables for user authentication and financial data. This separation ensures clarity and maintainability. Future scalability could involve migrating to a more robust database system like PostgreSQL, depending on the user base growth.


