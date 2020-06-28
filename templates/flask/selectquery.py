#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, desc

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Create a select query: stmt
stmt = select([flights.columns.destination, flights.columns.duration])

# Add a where clause to filter the results to only those for New York : stmt_filtered
stmt = stmt.order_by(flights.columns.destination, desc(flights.columns.duration))

# Execute the query to retrieve all the data returned: results
results = connection.execute(stmt).fetchall()

# Loop over the results and print the origin, destination, and duration
#for result in results:
    #print(result.origin, result.destination, result.duration)

print(results)
