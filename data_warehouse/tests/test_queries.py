from data_warehouse.sql_queries import create_table_queries, \
    drop_table_queries, copy_table_queries, insert_table_queries


def test_create_table_queries():
    for query in create_table_queries:
        print(query)
        assert query

def test_drop_table_queries():
    for query in drop_table_queries:
        print(query)
        assert query

def test_copy_table_queries():
    for query in copy_table_queries:
        print(query)
        assert query

def test_insert_table_queries():
    for query in insert_table_queries:
        print(query)
        assert query
