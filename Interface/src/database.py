import mysql.connector

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
        return

def disconnect(database):
    if database is not None:
        database.close()
        print("Closing database...")
    else:
        print("Database is already closed...")

def create_database(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("CREATE DATABASE {};".format(database_name))
    cursor.close()
    connect_database(database_name)

def execute_sql(db_connection, sql):
    cursor = db_connection.cursor()
    cursor.execute(sql)
    for x in cursor:
        print(x)
    cursor.close()
