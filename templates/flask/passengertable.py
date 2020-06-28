#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
passengers = Table('passengers', metadata, autoload=True, autoload_with=engine)

# Create a select query: stmt
stmt = select([passengers.columns.name, passengers.columns.flight_id])


# Execute the query to retrieve all the data returned: results
results = connection.execute(stmt).fetchall()

# Loop over the results and print the origin, destination, and duration
#for result in results:
    #print(result.origin, result.destination, result.duration)

print(results)
