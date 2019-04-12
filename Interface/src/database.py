import mysql.connector

def connect_database(database_name):
    try:
        print(0)
        connection = mysql.connector.connect(
            user    ="Group32",
            password="1234",
            database=database_name
        )
        return connection
    except:
        print(1)
        connection = mysql.connector.connect(
            user    ="Group32",
            password="1234"
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE {};".format(database_name))
        cursor.close()
        connect_database(database_name)

def disconnect(database):
    database.close()
    return

def execute_sql(db_connection, sql):
    cursor = db_connection.cursor()
    cursor.execute(sql)
    for x in cursor:
        print(x)
    cursor.close()
    return

db = connect_database("Airbnb")
execute_sql(db, "SHOW DATABASES;")
disconnect(db)
