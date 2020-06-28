# Project 1

Web Programming with Python and JavaScript

In this project, I built a book review website where users can search for any book using the book's isbn number, author, or title. In order to make a search, the users will have to register and then log in with their username
and password. After the users search for books, they will be able to see reviews made by other users, and they will be able to leave their own review. In this project, the user can also see the ratings pulled in from Goodreads.

application.py: This file is the main file of the project and contains the different routes for the book review website. This file contains the multiple queries using the users, books, and reviews table to the database.

import.py: In this file, I created the users, books, and reviews table. I also imported the books from the books.csv file into my books table.

testlogin.py: In this file, I created a function that makes sure that the user is logged in before they make searches on the website. If the user is not logged in, this function redirects them to the login page.

html files: Layout.html contains the base template for the rest of the html files and references the style.css file that I used for styling the website. Registration.html returns the form for the user to register by putting a username, password, and password confirmation. Login.html returns the form for the users to log in by inputting their username and password. It also returns the option to click the register button which redirects to the registration page if the user has not registered yet. Search.html returns the form for the users to input their book search using the book's title, author, or isbn number. Matches.html returns the title of every book that is similar to or matches the user's search input. Every match that is returned is linked to the book's details page. Book.html returns all of the details about the book and also returns reviews from other users. It displays the average rating and number of ratings the book has received from Goodreads, and it also allows the user to submit a review about the book.

style.css: This file is used for styling the website, and layout.html references the file in order to extend the styling to all of the html files.
