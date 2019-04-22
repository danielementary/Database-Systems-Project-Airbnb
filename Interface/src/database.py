import mysql.connector

from src.csv_tokenizer import tokenize_line

def connect_database(database_name):
    try:
        connection = mysql.connector.connect(
            user    ="Group32",
            password="1234",
            database=database_name
        )
        print("Connected to {} database".format(database_name))
        return connection
    except:
        print("Connection to {} database failed".format(database_name))
        try:
            connection = mysql.connector.connect(
                user    ="Group32",
                password="1234"
            )
            create_database(connection, database_name)
            disconnect(connection)
            return connect_database(database_name)
        except:
            print("Unable to create {} database".format(database_name),
                  "Please check that your MySQL is running and configured", sep="\n")

def disconnect(db_connection):
    if db_connection is not None:
        db_connection.close()
        print("Closing database...")
    else:
        print("Database is already closed...")

def create_database(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("CREATE DATABASE {} CHARACTER SET utf8;".format(database_name))
    cursor.close()
    print("Creating {} database".format(database_name))

def execute_sql(db_connection, sql, description):
    cursor = db_connection.cursor()
    try:
        cursor.execute(sql)
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably".format(description))
    cursor.close()

def execute_sql_list(db_connection, sql_list, description):
    cursor = db_connection.cursor()
    try:
        for sql in sql_list:
            cursor.execute(sql)
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably".format(description))
    cursor.close()

def count_tables(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'Airbnb';")
    count = None
    for x in cursor:
        count = x[0]
    cursor.close()
    return count

def populate_tables(db_connection, tables_to_populate, path_to_csv_dir):
    cursor = db_connection.cursor()

    for table_name in tables_to_populate:
        file = open(path_to_csv_dir+table_name+".csv", 'r')
        file.close()

    print("populate...")
