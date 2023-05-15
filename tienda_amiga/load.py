
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

from tienda_amiga.cfg import DATA_DIR, PG_CONN_ID

def load_to_postgres(table_name: str):
    df = pd.read_csv(DATA_DIR / "data_bitcoin_transformed.csv")
    hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    engine = hook.get_sqlalchemy_engine()
    df.to_sql(table_name, con=engine, if_exists='append')
