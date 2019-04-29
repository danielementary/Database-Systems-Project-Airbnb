import mysql.connector
import csv

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
            print("Unable to create or connect to {} database".format(database_name),
                  "Please check that your MySQL is running and configured", sep="\n")

def disconnect(db_connection):
    if db_connection is not None:
        db_connection.close()
    print("Disconnected from database")

def create_database(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("CREATE DATABASE {} CHARACTER SET utf8;"  .format(database_name))
    cursor.execute("set global max_allowed_packet=500000000;".format(database_name))
    cursor.close()
    print("Database {} created".format(database_name))

def execute_sql(db_connection, sql, description):
    cursor = db_connection.cursor()
    try:
        cursor.execute(sql)
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()

def execute_sql_list(db_connection, sql_list, description):
    cursor = db_connection.cursor()
    try:
        for sql in sql_list:
            cursor.execute(sql)
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()

def select_sql(db_connection, sql, description):
    cursor = db_connection.cursor()
    result = None
    try:
        cursor.execute(sql)
        print("{} executed successfully".format(description))
        result = cursor.fetchall()
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()
    return result

def select_sql_with_values(db_connection, sql, values, description):
    cursor = db_connection.cursor()
    result = None
    try:
        cursor.execute(sql, values)
        print("{} executed successfully".format(description))
        result = cursor.fetchall()
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()
    return result

def has_tables(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{}';".format(database_name))
    count = None
    for x in cursor:
        count = x[0]
    cursor.close()
    return (count > 0)

def every_table_has_entries(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.tables WHERE table_schema = '{}';".format(database_name))
    for x in cursor:
        if (x[1] <= 0):
            cursor.close()
            return False
    cursor.close()
    return True

def populate_tables(db_connection, tables_to_populate, path_to_csv_dir):
    cursor = db_connection.cursor()

    for table_name in tables_to_populate:
        print("Populating table {}".format(table_name))

        file = open(path_to_csv_dir+table_name+".csv", 'r', encoding='utf-8')
        reader = csv.reader(file, delimiter=",", quotechar="'")
        columns =  tuple(next(reader))

        sql = "INSERT INTO {} {} VALUES {}".format(table_name, columns, tuple(["%s" for _ in range(len(columns))])).replace("'", "")

        portion = 0
        values = []
        for row in reader:
            if (portion % 150000 == 0):
                cursor.executemany(sql, values)
                values = []
            portion += 1
            temp = [None if x == "NULL" else 0 if x == "0" else 1 if x == "1" else x for x in row]
            values.append(tuple(temp))

        cursor.executemany(sql, values)
        db_connection.commit()
        file.close()
        print("Table {} has been successfully populated".format(table_name))

    cursor.close()
