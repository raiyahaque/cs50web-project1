#Import SELECT
from sqlalchemy import select, create_engine, MetaData, Table, insert
from sqlalchemy.orm import scoped_session, sessionmaker
# Create an engine to the flights database
engine = create_engine('postgresql+psycopg2://localhost/flightsimulation')

# Create a connection on engine
connection = engine.connect()
db = scoped_session(sessionmaker(bind=engine))

#metadata = MetaData()

connection.execute("CREATE TABLE IF NOT EXISTS cost (id SERIAL PRIMARY KEY, payment INTEGER)")
connection.execute("INSERT INTO cost (payment) VALUES (:payment)", {"payment": 1200})
