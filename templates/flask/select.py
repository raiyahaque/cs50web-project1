#Import SELECT
from sqlalchemy import select, MetaData, Table, create_engine

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

#Build select statement for flights table: stmt
stmt = select([flights])

# Print the emitted statement to see the SQL string
#print(stmt)

# Execute the statement on connection and fetch 10 records: result
results = connection.execute(stmt).fetchmany(size=10)

# Execute the statement and print the results
#print(results)

# Get the first row of the results by using an index: first_row
first_row = results[0]

# Print the first row of the results
print(first_row)

# Print the 'state' column of the first row by using its name
print(first_row['origin'])
