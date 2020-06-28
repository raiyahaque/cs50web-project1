# Import create_engine function

from sqlalchemy import create_engine, MetaData, Table

#import psycopg2

# Create an engine to the census database

engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a metadata object: metadata
metadata = MetaData()

# Reflect census table from the engine: census
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Print the column names
print(flights.columns.keys())

# Print census table metadata
#print(repr(flights))

# Use the .table_names() method on the engine to print the table names

#print(engine.table_names())
