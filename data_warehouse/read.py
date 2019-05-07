def read_sql_query(filepath):
    with open(filepath, "r") as file_pointer:
        return file_pointer.read()
