import mysql.connector

# db = mysql.connector.connect(
#     user="Group32",
#     password="1234"
# )
#
# cursor = db.cursor

def connect_database(database_name):
    return mysql.connector.connect(
        user="Group32",
        password="1234",
        database=database_name
    )

def create_cursor(db):
    return db.cursor();

def create_database(cursor, database_name):
    sql = "CREATE DATABASE {}".format(database_name)
    cursor.execute(sql)

def close_database(database):
    database.close()

db = connect_database("test")
db.close()
