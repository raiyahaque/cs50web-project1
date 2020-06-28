#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)
passengers = Table('passengers', metadata, autoload=True, autoload_with=engine)

# Build a statement to select the flights and passengers tables: stmt
#stmt = select([flights, passengers])

#stmt_join = stmt.select_from(flights.join(passengers, flights.columns.id == passengers.columns.flight_id))

#results = connection.execute(stmt_join).fetchall()

results = connection.execute("SELECT * FROM flights JOIN passengers ON passengers.flight_id = flights.id WHERE name = 'Alice'").fetchall();

#print(results)
for record in results:
    print(record)
