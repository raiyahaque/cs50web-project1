#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, and_

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Create a select query: stmt
stmt = select([flights])

# Append a where clause to select only non-male records from California using and_
stmt = stmt.where(
    # The state of California with a non-male sex
    and_(flights.columns.origin == 'New York',
         flights.columns.duration >= 200
         )
)

# Loop over the ResultProxy printing the age and sex
for result in connection.execute(stmt):
    print(result.origin, result.destination, result.duration)
