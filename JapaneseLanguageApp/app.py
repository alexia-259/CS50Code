import os

from cs50 import SQL
from datetime import date, timedelta
import random
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)
app.secret_key = "sss"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///projects.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return redirect("/home")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Please provide a username")
            return render_template("login.html")

        if not password:
            flash("Please provide a password")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1:
            flash("Username not found")
            return render_template("login.html")

        user = rows[0]

        if not check_password_hash(user["hash"], password):
            flash("Incorrect password")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        db.execute("UPDATE users SET times_logged = times_logged + 1 WHERE id = ?",( user["id"]))
        return redirect("/dashboard")

    # GET request
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("No username")
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            flash("No password")
            return render_template("register.html")

        elif password != confirmation:
            flash("Passwords do not match")
            return render_template("register.html")

        hashed_pass = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash, name) VALUES (?, ?, ?)", username, hashed_pass, name)
        except ValueError:
            flash("invalid username and/or password")
            return render_template("register.html")


        return redirect("/login")
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    today = date.today().isoformat()
    result = db.execute("SELECT name, times_logged FROM users WHERE id = ?", (user_id))
    streak = db.execute("SELECT streak_count FROM lesson WHERE user_id = ?",  (user_id))

    if not streak:
        db.execute("INSERT INTO lesson (user_id, last_active) VALUES (?,?)", user_id, today)
        streak = db.execute("SELECT streak_count FROM lesson WHERE user_id = ?", (user_id))


    if result:
        name = result[0]["name"].capitalize()
        time = result[0]["times_logged"]
    else:
        name = None
        time = 1

    streak_count = streak[0]["streak_count"]
    return render_template("dashboard.html", name = name, time = time, streak = streak_count)


@app.route('/review', methods=["GET", "POST"])
@login_required
def review():
    user_id = session["user_id"]
    today = date.time().isofromat()
    now = datetime.utcnow()

    lesson_data = db.execute("SELECT lessons_done, last_review_time, review_count, last_active,streak_count FROM lesson WHERE user_id = ?", user_id)

    lessons_done = lesson_data[0]["lesson_done"]
    review_count = lesson_data[0]["review_count"]
    last_review_time = lesson_data[0]["last_review_time"]
    last_active = lesson_data[0]["last_active"]
    streak = lesson_data[0]["streak"]

    if no last_active:
        flash("No lesson data found. Do a lesson first!")
        return redirect("/dashboard")

    if request.method == "POST";
    data = request.get.json()
    mistakes = data.get("mistakes", [])

    for m in mistakes:
        db.execute("INSERT INTO mistakes (user_id, hiragana, romaji) VALUES (?, ?, ?)"
                    user_id, m["hiragana"], m["romaji"])



@app.route("/freereview")
@login_required
def free_review():
    questions = db.execute("SELECT * FROM hiragana ORDER BY RANDOM() LIMIT 10")
    return render_template("freereview.html", questions = questions)

@app.route("/log_mistake", methods = ["POST"])
def log_mistake():
    user_id = session["user_id"]
    data = request.get_json()
    hiragana = data.get("hiragana")
    romaji = data.get("romaji")

    db.execute("INSERT INTO lesson (mistakes, user_id, romaji) VALUES (?,?, ?)", hiragana, user_id, romaji)
    return jsonify(success = True), 200

@app.route("/mistake")
@login_required
def mistake():
    user_id = session["user_id"]
    mistakes = db.execute("SELECT * FROM lesson WHERE user_id = ? ORDER BY created_at DESC", user_id)

    return render_template("recentmistake.html", mistakes = mistakes)

@app.route('/go_lesson', methods=["GET", "POST"])
@login_required
def go_lesson():
    user_id = session["user_id"]
    lesson = db.execute("SELECT lessons_done FROM lesson WHERE user_id = ?", user_id)

    if len(lesson) == 0:
        db.execute("INSERT INTO lesson (user_id) VALUES (?)", user_id)
        lesson = db.execute("SELECT lessons_done FROM lesson WHERE user_id = ?", user_id)

    times = lesson[0]["lessons_done"]

    return redirect(f'/lesson/{times}')

@app.route('/lesson/<int:lesson_number>')
@login_required
def lesson(lesson_number):
    template_name = f"lesson{lesson_number}.html"

    return render_template(template_name)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")
