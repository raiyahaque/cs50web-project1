#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, func, case, cast, Float

# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()

metadata = MetaData()

#Reflect flights table via engine: flights
flights = Table('flights', metadata, autoload=True, autoload_with=engine)

# Build an expression to calculate duration sum in New York
duration_sum = func.sum(
    case([
        (flights.columns.origin == 'New York', flights.columns.duration)
    ], else_=0))

# Cast an expression to calculate total duration time to Float
total_duration = cast(func.sum(flights.columns.duration), Float)

#query to calculate how much of duration time is from new york flights
stmt = select([duration_sum / total_duration * 100])

percent_newyork = connection.execute(stmt).scalar()

print(percent_newyork)
