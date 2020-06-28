import os
import json
import requests

from flask import Flask, session, request, render_template, jsonify, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from testlogin import login_required
from werkzeug.security import check_password_hash, generate_password_hash

#make connection to the database and its information
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))


app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    session.clear()
    #return search form
    return render_template("search.html", message="Search any book using its ISBN number, title, or author.")


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    """Register!"""
    if request.method == 'POST':
        # Get username
        user_username = request.form.get("username")
        # Get password
        user_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if confirm_password == user_password and user_username != None and user_password != None:
            # Check if username is unique
            if db.execute("SELECT * FROM users WHERE usernames = :user_username", {"user_username": user_username}).rowcount == 0:
                db.execute("INSERT INTO users (usernames, passwords) VALUES (:usernames, :passwords)",
                        {"usernames": user_username, "passwords": generate_password_hash(user_password)})
                db.commit()
                return render_template("login.html", message="Login with username and password.")
            else:
                # If not unique, then return registration template again
                error = "This username is already taken. Please enter a different username."
                flash(error)
                return redirect("/registration")
        return render_template("login.html", message="Login with username and password!")
    else:
        return render_template("registration.html", message="Register Now!")


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        login_username = request.form.get("username")
        login_password = request.form.get("password")
        error = None
        # Select the row where the username matches a user in the users table
        table_user = db.execute("SELECT * FROM users WHERE usernames = :login_username", {"login_username": login_username}).fetchone()
        # If the user doesn't exist or is incorrect
        if table_user is None:
            error = "Incorrect username or username does not exist."
            # Check if password is correct
        elif not check_password_hash(table_user['passwords'], login_password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            # set user id in session user_id
            session['user_id'] = table_user['id']
            session['user_name'] = table_user['usernames']
            if session['user_name'] != None:
                currentUsername = 'Hi, ' + session['user_name']
            return render_template("search.html", message="Search any book using its ISBN number, title, or author.", currentUsername=currentUsername)

        flash(error)

    return render_template("login.html", message="Login with username and password.")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    if session['user_name'] != None:
        currentUsername = 'Hi, ' + session['user_name']
    # Save user's search input from the form in a variable
    user_search = ('%' + request.form.get("Search") + '%').lower()

    # Query for results where user's search matches or is like book's author, title, or isbn number
    results = db.execute("SELECT * FROM books WHERE LOWER(author) LIKE :user_search OR LOWER(title) LIKE :user_search OR isbn LIKE :user_search",
                    {"user_search": user_search}).fetchall()

    # No results found
    if len(results) == 0:
        error = "No matches found."
        flash(error)
        return render_template("search.html", message="Search any book using its ISBN number, title, or author.")
    else:
        # Return all possible results
        return render_template("matches.html", matches=results, currentUsername=currentUsername)

@app.route("/book/<string:book_title>", methods=['GET', 'POST'])
@login_required
def book_details(book_title):
    if session['user_name'] != None:
        currentUsername = 'Hi, ' + session['user_name']
    if request.method == "POST":
        currentUser = session['user_id']
        # Get user's rating of the book
        review_rating = int(request.form.get("Rating"))
        # User's comment about the book
        review_comment = request.form.get("Review")
        # Get book's id where book title matches the chosen book's title
        row = db.execute("SELECT id FROM books WHERE title = :book_title", {"book_title": book_title}).fetchone()
        title = db.execute("SELECT title FROM books WHERE title = :book_title", {"book_title": book_title}).fetchone()
        bookId = row[0]
        # Check if user has made a review for the book already
        if db.execute("SELECT * FROM reviews WHERE user_id = :currentUser AND book_id = :bookId", {"currentUser": currentUser, "bookId": bookId}).rowcount == 0:
            db.execute("INSERT INTO reviews (book_id, user_id, rating, comment) VALUES(:book_id, :user_id, :rating, :comment)",
                        {"book_id": bookId, "user_id": currentUser, "rating": review_rating, "comment": review_comment})
            db.commit()
        else:
            # User has already made a review for this book
            flash("You have already submitted a review for this book.")
            return redirect(url_for('book_details', book_title=title[0]))

        return redirect(url_for('book_details', book_title=title[0]))

    else:
        row = db.execute("SELECT id FROM books WHERE title = :book_title", {"book_title": book_title}).fetchone()
        bookId = row[0]
        # Query for all of the book details
        booksearches = db.execute("SELECT * FROM books WHERE title = :book_title", {"book_title": book_title}).fetchall()
        # Query for all of the reviews of the book
        book_reviews = db.execute("SELECT usernames, rating, comment FROM users INNER JOIN reviews ON users.id = reviews.user_id WHERE book_id = :bookId", {"bookId": bookId}).fetchall()
        isbn_num = db.execute("SELECT isbn FROM books WHERE title = :book_title", {"book_title": book_title}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4H93fcjlbQieCpjM6pOetg", "isbns": isbn_num})
        data = res.json()
        # Goodreads ratings count
        book_ratings_count = data['books'][0]['ratings_count']
        # Goodreads average rating
        book_avg_rating = data['books'][0]['average_rating']
        return render_template("book.html", booksearches=booksearches, book_reviews=book_reviews, book_avg_rating=book_avg_rating, book_ratings_count=book_ratings_count, currentUsername=currentUsername)

@app.route("/api/<string:isbn>", methods=['GET'])
def api_access(isbn):
    # Check if isbn is valid
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return jsonify({"error": "Invalid isbn."}), 404
    # Check if book has a review; if no review, set review count to 0 and average score to 0
    elif db.execute("SELECT * FROM reviews INNER JOIN books ON reviews.book_id = books.id WHERE books.isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        book_review_count = 0;
        book_average_score = 0;
        results = db.execute("SELECT title, author, year, isbn FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        return jsonify({
            "title": results['title'],
            "author": results['author'],
            "year": results['year'],
            "isbn": results['isbn'],
            "review_count": book_review_count,
            "average_score": book_average_score})
    else:
        # Select title, author, year, isbn, review count, and average score of the book
        row = db.execute("SELECT title, author, year, isbn, COUNT(reviews.id) AS review_count, AVG(reviews.rating) AS average_score FROM books INNER JOIN reviews ON books.id = reviews.book_id WHERE books.isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn}).fetchone()

        results = dict(row.items())

        results['average_score'] = float("%.2f"%(results['average_score']))

        return jsonify({
        "title": results['title'],
        "author": results['author'],
        "year": results['year'],
        "isbn": results['isbn'],
        "review_count": results['review_count'],
        "average_score": results['average_score']
        })
