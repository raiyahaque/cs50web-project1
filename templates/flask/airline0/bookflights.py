from sqlalchemy import create_engine, MetaData, Table, select, insert
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)
passengers = Table('passengers', metadata, autoload=True, autoload_with=engine)

@app.route("/")
def index():
    flights = connection.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    if connection.execute("SELECT * FROM flights WHERE id = flights.id").rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")
    connection.execute(insert(passengers).values(name = name, flight_id = flight_id))
    #connection.commit()
    return render_template("success.html")


@app.route("/flights")
def flights():
    flights = connection.execute("SELECT * FROM flights").fetchall()
    print(flights)
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = connection.execute("SELECT * FROM flights WHERE id = flights.id").fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight.")

    passengers = connection.execute("SELECT name FROM passengers WHERE passengers.flight_id = flight_id").fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
