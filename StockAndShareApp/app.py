import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    rows = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    portofolio = []
    stock_value = 0

    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]

        quote = lookup(symbol)

        price = quote["price"]
        total_value = price * shares
        stock_value += total_value

        portofolio.append({"symbol": symbol, "name": quote["name"], "shares": shares, "price": price, "total": total_value})

    assets = user_cash + stock_value

    return render_template("index.html", portofolio = portofolio, cash = usd(user_cash), total = usd(assets))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology ("Shares requires a positive integer", 400)

        shares = int(shares)
        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol", 400)
        price = quote["price"]

        total_price = shares * price

        row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        cash = row[0]["cash"]

        if cash < total_price:
            return apology("not enough funds for ransactions")

        new_price = cash - total_price
        transaction_type = "Buy"
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_price, session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, buy_sell) VALUES (?,?,?,?,?)",session["user_id"], symbol, shares, price, transaction_type)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transaction_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions = transaction_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("No quote given", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("Not a valid stock symbol", 400)

        return render_template("quoted.html" , quote = quote)

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        elif password != confirmation:
            return apology("Passwords do not match", 400)

        hashed_pass = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_pass)

        except ValueError:
            return apology("Username already in use")

        return redirect("/login")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":

        rows = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        symbols = []
        for row in rows:
            symbols.append(row["symbol"])
        return render_template("sell.html", symbols = symbols)

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must Give Symbol")

        if not shares or not shares.isdigit():
            return apology("Shares must be a positive integer", 400)

        shares = int(shares)

        owned_shares = db.execute("SELECT SUM(shares) AS total FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)

        if not owned_shares:
            return apology("You don't own those shares", 400)

        if shares > owned_shares[0]["total"]:
            return apology("Not that many shares owned", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("Invalid stock symbol", 400)

        price = quote["price"]
        sale_value = shares * price

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, buy_sell) VALUES (?, ?, ?, ?, ?)", user_id, symbol, -shares, price, "Sell")
        row = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        cash = row[0]["cash"]

        return render_template("sell.html", sale_value = sale_value , cash = cash)
