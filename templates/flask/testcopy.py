# Import create_engine function

from sqlalchemy import create_engine, MetaData, Table

#import psycopg2

# Create an engine to the census database

engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

# Build select statement for census table: stmt
#stmt = 'SELECT * FROM flights'

# Execute the statement and fetch the results: results
#results = connection.execute(stmt).fetchall()

flights = connection.execute("SELECT origin, destination, duration FROM flights").fetchall()
for flight in flights:
    print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

# Print results
#print(results)
