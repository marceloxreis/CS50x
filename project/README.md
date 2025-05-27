# My finance
#### Video Demo:  <[URL HERE](https://youtu.be/9lpXkQbDmhQ) >
#### Description:---
## Finance Management Web Application

### Project Overview

This **Finance Management Web Application** is engineered to empower users in monitoring and managing their personal finances. Developed with **Python** and the **Flask framework**, it offers a user-friendly interface for **tracking expenses**, **viewing cash balances**, and **categorizing transactions**. The backend efficiently stores and retrieves data using **SQLite**, while the frontend utilizes **Flask templates** for dynamic content rendering. **Security** is foundational, incorporating **password hashing** and **session management** to safeguard user information.

The application includes the following core functionalities:

* **User Registration and Authentication:** New users can securely create accounts, and existing users can log in and out with robust hashed password storage and validation.
* **Dashboard Overview:** Provides an immediate display of the user's current cash balance and detailed spending records, effectively categorized by type.
* **Expense Logging:** Users can log new expenses, which are automatically subtracted from their available cash and persistently stored in the database.
* **Cash Balance Editing:** Offers the flexibility for users to directly update their total cash balance as needed.
* **Transaction Management:** Enables users to remove specific transactions, with the application automatically adjusting the available cash amount to reflect the change.

The application is built to be intuitive, yet delivers robust features for effective financial data management.

---

### File Descriptions

#### `app.py`
As the primary application file, `app.py` contains all Flask routes, handling user requests and database interactions. Its key components include:
* **Session Configuration:** Utilizes Flask-Session to manage user sessions securely, storing session data on the file system rather than in browser cookies.
* **Routes:** Manages core application functionalities:
    * `/` (Index Route): Displays the user's current cash balance and categorized expenses, querying `user_data` for transactions and `users` for the cash balance.
    * `/login`: Handles user login, validating credentials against the database. Successful logins initiate a user session and redirect to the index page; error messages are displayed for incorrect inputs.
    * `/logout`: Clears the user session and redirects to the login page.
    * `/register`: Manages new user registration by validating form inputs, hashing passwords, checking for existing usernames, and storing new user details in the `users` table. Successful registration redirects the user to the login page.
    * `/buy`: Allows users to add new expenses. It validates category and amount, ensures sufficient cash, and updates the database, adjusting the cash balance and logging the transaction in `user_data`.
    * `/edit`: Facilitates direct updates to the cash balance by allowing users to input a new amount, which is then updated in the `users` table.
    * `/remove`: Deletes a specific transaction from `user_data`, automatically adding the transaction amount back to the cash balance. This route ensures only authorized users can delete their own transactions.

#### `helpers.py`
This file contains utility functions used throughout the application:
* `apology`: Renders custom error messages for user mistakes or system errors.
* `login_required`: A decorator restricting access to specific routes, ensuring only authenticated users can view or interact with certain pages.
* `lookup`: A stub function intended for future integration with financial APIs to look up data.
* `usd`: A custom filter for consistently formatting numbers as USD currency.

#### `finance.db`
The SQLite database file responsible for maintaining all user and financial information:
* `users`: Stores user details, including `id`, `username`, and a hashed `password` for secure authentication.
* `user_data`: Records expenses with columns for `user_id`, `category`, `amount`, and a unique `transaction id`, facilitating efficient expense tracking and management.

#### `templates/`
This directory houses the HTML templates rendered by Flask, providing a dynamic user experience:
* `index.html`: Displays the user's financial summary, including cash balance and categorized expenses, offering a clear view of their financial status.
* `login.html`: A form for user login, including validation messages for incorrect inputs.
* `register.html`: A form for new user registration, with fields for username, password, and confirmation, and feedback for validation errors.
* `buy.html`: A form for adding expenses, allowing users to input a category and amount, with data validation ensuring positive amounts within available cash.
* `edit.html`: A form for updating the cash balance, where the user inputs a new balance for database update.
* `apology.html`: Used to consistently display error messages, ensuring a user-friendly experience when issues occur.

---

### Design Decisions

#### Security
**Password security** is paramount, achieved through hashing with `generate_password_hash` and validation with `check_password_hash` from `werkzeug.security`. **Session management** is secure, with data stored on the file system rather than in browser cookies, enhancing protection. Additionally, access to routes is strictly controlled for authenticated users via the `login_required` decorator.

#### User Experience
The application is designed with a **simple and intuitive interface** for finance management. The decision to allow direct editing of the cash balance streamlines user input, though future enhancements could include detailed audit trails or more granular tracking. **Flash messages** and **error handling** provide immediate feedback, guiding the user through various operations.

#### Database Structure
The database schema is **optimized for quick and efficient lookups**, utilizing separate tables for user authentication and financial data. This separation ensures both clarity and maintainability. Future scalability considerations include potential migration to a more robust database system like PostgreSQL, contingent on user base growth.
