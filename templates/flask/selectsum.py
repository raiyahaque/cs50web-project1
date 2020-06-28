#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, func

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Calculate sum of duration
duration_sum = func.sum(flights.columns.duration).label('duration')

# Query to select origin and duration sum
stmt = select([flights.columns.origin, duration_sum])

# Group stmt by origin
stmt = stmt.group_by(flights.columns.origin)

# Execute the statement and store all the records: results
results = connection.execute(stmt).fetchall()

# Print results
print(results)

# Print the keys/column names of the results returned
print(results[0].keys())
