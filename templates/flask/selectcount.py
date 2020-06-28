#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, func

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Build a query to select the state and count of ages by state: stmt
stmt = select([flights.columns.destination, func.count(flights.columns.duration)])

# Group stmt by state
stmt = stmt.group_by(flights.columns.destination)

# Execute the statement and store all the records: results
results = connection.execute(stmt).fetchall()

# Print results
print(results)

# Print the keys/column names of the results returned
print(results[0].keys())
