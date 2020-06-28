#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, insert
import csv

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

f = open("flights.csv")
reader = csv.reader(f)

for origin, destination, duration in reader:
    connection.execute(insert(flights).values(origin = origin, destination = destination, duration = duration))


print(connection.execute(select([flights]).where(flights.columns.duration == 200)).fetchall())
