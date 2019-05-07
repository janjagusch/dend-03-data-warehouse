from data_warehouse import aws, create_tables, etl


def main():
    aws.main()
    create_tables.main()
    etl.main()
    print("Done.")
