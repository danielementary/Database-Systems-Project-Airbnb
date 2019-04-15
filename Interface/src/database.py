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
    print("Creating database : {}".format(database_name))

def drop_database(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("DROP DATABASE {};".format(database_name))
    cursor.close()
    print("Dropping database : {}".format(database_name))

def create_table(db_connection, table_name, fields):
    cursor = db.connection.cursor()
    sql = "CREATE TABLE {} ("
    for f in fields:
        sql += f
    sql += ");"
    cursor.execute(sql)
    cursor.close()
    print("Creating table : {}".format(sql))

def drop_table(db_connection, table_name):
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE {};".format(table_name))
    cursor.close()
    print("Dropping table : {}".format(table_name))

def execute_sql(db_connection, sql):
    cursor = db_connection.cursor()
    cursor.execute(sql)
    for x in cursor:
        print(x)
    cursor.close()
