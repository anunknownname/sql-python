import sqlite3
with sqlite3.connect("sql-python/database_creation_folder/sql.db") as database:
    cursor = database.cursor()
    def new_table():
        while True:
            try:
                new_table_name = input("Creating a new table...\n New table name? ")
                initial_column_name = input("First column name? ")
                initial_column_datatype = input("First column data type. Enter INTEGER for a number, or TEXT for a word. ")
                values = initial_column_name.lower() + " " + initial_column_datatype.upper()
                cursor.execute(f"DROP TABLE IF EXISTS {new_table_name};")
                cursor.execute(f"CREATE TABLE {new_table_name} ({values})")
                print("New table successfully created")
                break
            except:
                print("Invalid input, try again...")
    def new_columns():
        while True:
            try:
                editing_table = input("Editing an existing table... \n Enter table to edit: ")
                editing_columns_name = input("Enter a column name you wish to create: ")
                editing_columns_datatype = input("Enter the new columns datatype. Enter INTEGER for a number, or TEXT for a word: ")
            except:
                pass
