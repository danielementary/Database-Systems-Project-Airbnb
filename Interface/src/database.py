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
        connection.autocommit = True
        return connection
    except:
        print("Connection to {} database failed".format(database_name))
        try:
            connection = mysql.connector.connect(
                user    ="Group32",
                password="1234"
            )
            create_database(connection, database_name)
            connection.close()
            return connect_database(database_name)
        except:
            print("Unable to create or connect to {} database".format(database_name),
                  "Please check that your MySQL is running and configured", sep="\n")
            return None

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
    for sql in sql_list:
        try:
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
        result = cursor.fetchall()
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()
    return result

def select_sql_with_values(db_connection, sql, values, description):
    cursor = db_connection.cursor()
    result = None
    try:
        cursor.execute(sql, values)
        result = cursor.fetchall()
        print("{} executed successfully".format(description))
    except:
        print("{} failed miserably"     .format(description))
    cursor.close()
    return result

def has_tables(db_connection, number_of_tables, database_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{}';".format(database_name))
    count = 0
    for x in cursor:
        count = x[0]
    cursor.close()
    return (count == number_of_tables)

def every_table_has_entries(db_connection, database_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT TABLE_NAME, SUM(TABLE_ROWS) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}' GROUP BY TABLE_NAME;".format(database_name))
    result = True
    for x in cursor:
        if (x[1] <= 0):
            result = False
    cursor.close()
    return result

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
            if (portion % 250000 == 0):
                cursor.executemany(sql, values)
                values = []
            temp = tuple([None if x == "NULL" else 0 if x == "0" else 1 if x == "1" else x for x in row])
            values.append(temp)
            portion += 1
        cursor.executemany(sql, values)
        file.close()
        print("Table {} has been successfully populated".format(table_name))
    cursor.close()
    print("Database has been successfully populated")

def insert_listing(db_connection, values):
    cursor = db_connection.cursor()
    sql = "INSERT INTO Listing (listing_id, listing_name, listing_summary, accommodates, square_feet, price, \
                                host_id, neighbourhood_id, property_type_id, room_type_id, bed_type_id, \
                                cancellation_policy_id) VALUES {}".format(tuple(values))
    cursor.execute(sql)
    cursor.close()
    print("Listing {} has been successfully inserted by {}".format(values[0], values[-6]))

def insert_host(db_connection, values):
    cursor = db_connection.cursor()
    sql    = "INSERT INTO Host (host_id, host_name, neighbourhood_id)  VALUES {}".format(tuple(values))
    cursor.execute(sql)
    cursor.close()
    print("Host {} has been successfully inserted".format(values[1]))

def insert_neighboorhood(db_connection, values):
    cursor = db_connection.cursor()
    sql    = "INSERT INTO Neighbourhood (neighbourhood_id, neighbourhood_name, city_id) VALUES {}".format(tuple(values))
    cursor.execute(sql)
    cursor.close()
    print("Neighbourhood {} has been successfully inserted".format(values[1]))
