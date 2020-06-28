from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://localhost/stationstates')

print(engine.table_names())
