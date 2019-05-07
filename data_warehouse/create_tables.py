from data_warehouse.db import connect
from data_warehouse.sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main(verbose=False):
    cur, conn = connect()
    if verbose:
        print("Dropping tables...")
    drop_tables(cur, conn)
    if verbose:
        print("Creating tables...")
    create_tables(cur, conn)
    if verbose:
        print("Done.")
    conn.close()
