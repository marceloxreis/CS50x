import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    """Display user's stocks and cash balance."""

    # Get the user ID from the session
    user_id = session["user_id"]

    # Query the database to get the stocks owned by the user and the total shares for each stock
    user_stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM purchases
        WHERE user_id = ?
        GROUP BY symbol
        """, user_id)
    # Initialize a list to hold the stock information
    stocks = []

    # Calculate the total value of the user's holdings
    total_value = 0

    for stock in user_stocks :
        if stock["total_shares"] > 0:
            symbol = stock["symbol"]
            shares = stock["total_shares"]
            stock_info = lookup(symbol)
            current_price = stock_info["price"]
            total_cost = current_price * shares
            total_value += total_cost
            stocks.append({
                "symbol": symbol,
                "shares": shares,
                "current_price": current_price,
                "total_cost": total_cost
            })

    # Query the database to get the user's current cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate the grand total (stocks' total value + cash)
    grand_total = total_value + user_cash

    # Render the index page with the user's stock holdings
    return render_template("index.html", stocks=stocks, cash=user_cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        symbol = request.args.get("symbol")
        return render_template("buy.html", symbol=symbol)
    if request.method == "POST":
        # Check if stock symbol is provided
        if not request.form.get("symbol"):
            return apology("must provide correct symbol", 403)

        # Get and validate shares input
        shares = request.form.get("shares")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive shares", 400)

        # Get stock information
        stock = lookup(request.form.get("symbol"))
        if stock is None:
            return apology("invalid symbol", 400)

        # Get user's available cash
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Calculate total cost
        total_cost = stock["price"] * int(shares)

        if total_cost > user_cash:
            return apology("not enough cash", 400)

        # Log the purchase and update user cash
        try:
            # Insert purchase details into 'purchases' table
            db.execute("INSERT INTO purchases (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                       user_id, stock["symbol"], int(shares), stock["price"])

            # Deduct cash from user's account
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        except Exception as e:
            return apology("error occurred while processing your purchase", 500)

        # Redirect to homepage
        flash("Buy is successfully")
        return redirect("/")

    # If GET request, render the buy form
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # Query transactions from the transactions table
    transactions = db.execute("""
        SELECT symbol, shares, price, date FROM purchases
        WHERE user_id = ?
        ORDER BY date DESC
        """, user_id)

    # Render the history template with the transactions
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Display stock quote form and handle quote lookup."""

    # If the form was submitted
    if request.method == "POST":

        # Get the stock symbol from the form
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must provide symbol", 400)

        # Look up the stock's current price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        # If a valid stock is found, render the result page
        if stock:
            return render_template("quoted.html", stock=stock)

        # Show an error if the stock symbol is invalid
        else:
            return apology("Invalid symbol", 400)

    # Display the quote input form if the request method is GET
    return render_template("quote.html")


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
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(existing_user) > 0:
            return render_template("register.html", message="Username already exists"), 400

        # If all checks pass, hash the password and store the new user
        password_hash = generate_password_hash(password)

        # Try to insert the new user into the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        except sqlite3.IntegrityError:
            return render_template("register.html", message="An error occurred. Please try again."), 500

        # Redirect to login page after successful registration
        flash("Registration successful! Please log in.")
        return redirect("/login")

    else:
        # If GET request, render the register form
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "GET":
        symbol = request.args.get("symbol")
        return render_template("sell.html", symbol=symbol)

    if request.method == "POST":
        # Check if stock symbol is provided

        if not request.form.get("symbol"):
            return apology("must provide correct symbol", 400)

        # Get and validate shares input
        shares = request.form.get("shares")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive shares", 400)

        # Get stock information
        stock = lookup(request.form.get("symbol"))
        if stock is None:
            return apology("invalid symbol", 400)

        # Get user's available cash

        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, stock["symbol"])
        if not user_shares or user_shares[0]["total_shares"] < int(shares):
            return apology("not enough shares", 400)
        # Calculate total value
        total_value = stock["price"] * int(shares)

        # Log the purchase and update user cash
        try:
            # Insert purchase details into 'purchases' table
            db.execute("INSERT INTO purchases (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                       user_id, stock["symbol"], -int(shares), stock["price"])

            # Deduct cash from user's account
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)
        except Exception as e:
            return apology("an error occurred while processing your sale", 500)
        flash("Sell is successfully")
        return redirect("/")
    else:
        # Render the sell form
        return render_template("sell.html")
