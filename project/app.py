import os
import sqlite3
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Display user's categories and cash balance."""

    # Get the user ID from the session
    user_id = session["user_id"]

    # Query the database to get the spending categories and amounts
    user_data = db.execute("""
        SELECT category, amount, id
        FROM user_data
        WHERE user_id = ?
        """, user_id)

    # Get the user's available cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Render the index page with user data and cash balance
    return render_template("index.html", user_data=user_data, cash=user_cash)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # If user is already logged in, render the index page directly
    if session.get("user_id"):
        return index()  # Render index page directly if already logged in

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Instead of redirecting, render the index page directly with the necessary data
        flash("Logged in successfully")
        return redirect("/") # Call the `index` function directly to render it

    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return render_template("register.html", message="Must provide username"), 400

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return render_template("register.html", message="Must provide password"), 400

        # Ensure password confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return render_template("register.html", message="Must confirm password"), 400

        # Check if passwords match
        if password != confirmation:
            return render_template("register.html", message="Passwords do not match"), 400

        # Check if the username already exists in the database
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username,)
        if len(existing_user) > 0:
             return apology("Username already exists", 400)

        # Store form inputs
        password_hash = generate_password_hash(password)

        # Try to insert the new user into the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        except sqlite3.IntegrityError:
            return render_template("register.html", message="Username already exists"), 400

        # Redirect to login page after successful registration
        flash("Registration successful! Please log in.")
        return redirect("/login")

    else:
        # If GET request, render the register form
        return render_template("register.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Get and validate category and amount inputs
        category = request.form.get("category")
        amount = request.form.get("amount")

        if not category:
            return apology("must provide category", 400)
        if not amount or not amount.isdigit() or int(amount) <= 0:
            return apology("must provide positive amount", 400)

        # Get user's available cash
        user_id = session["user_id"]
        result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = result[0]["cash"] if result else 0

        # Calculate total cost
        total_cost = int(amount)

        if total_cost > user_cash:
            return apology("not enough cash", 400)


        # Log the purchase and update user cash
        try:
            # Insert purchase details into 'user_data' table
            db.execute("INSERT INTO user_data (user_id, category, amount) VALUES (?, ?, ?)",
                       user_id, category, total_cost)

            # Deduct cash from user's account
            db.execute("UPDATE users SET cash = cash - ?  WHERE id = ?", total_cost, user_id)
        except Exception as e:
            return apology("error occurred while processing your purchase", 500)

        # Redirect to homepage
        flash("Buy is successful")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        # Get and validate category and amount inputs
        amount = request.form.get("amount")

        try:
            amount = float(amount)
            if amount <= 0:
                return apology("must provide positive amount", 400)
        except ValueError:
            return apology("invalid amount", 400)

        # Get user's available cash (not needed for editing directly, but kept in case)
        user_id = session["user_id"]

        # Set the new cash balance directly
        new_cash_balance = int(amount)

        # Update user cash
        try:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)
        except Exception as e:
            return apology(f"Database error: {e}", 500)

        flash("Edit is successful")
        return redirect("/")

    # Handle GET request (if necessary)
    return render_template("edit.html")



@app.route("/remove", methods=["POST"])
@login_required
def remove():
    """Remove a user's transaction and update cash balance"""
    # Get the transaction ID from the form
    transaction_id = request.form.get("transaction_id")

    if not transaction_id:
        return apology("Transaction ID is required", 400)

    # Validate that the transaction belongs to the logged-in user
    user_id = session["user_id"]
    transaction = db.execute("""
        SELECT * FROM user_data
        WHERE id = ? AND user_id = ?
        """, transaction_id, user_id)

    if len(transaction) != 1:
        return apology("Transaction not found or unauthorized", 403)

    # Retrieve the amount to add back to the user's cash
    amount_to_add = transaction[0]["amount"]

    # Update the user's cash balance
    try:
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount_to_add, user_id)
        # Delete the transaction
        db.execute("DELETE FROM user_data WHERE id = ?", transaction_id)
    except Exception as e:
        return apology("Error occurred while deleting the transaction", 500)

    flash("Transaction removed successfully, and cash balance updated")
    return redirect("/")

