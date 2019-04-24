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
    cursor.execute("set global max_allowed_packet=500000000;".format(database_name))
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
        xyz = 0
        file = open(path_to_csv_dir+table_name+".csv", 'r', encoding='utf-8')
        reader = csv.reader(file, delimiter=",", quotechar="'")
        columns =  tuple(next(reader))

        sql = "INSERT INTO {} {} VALUES {}".format(table_name, columns, tuple(["%s" for _ in range(len(columns))])).replace("'", "")

        values = []
        for row in reader:
            temp = [None if x == "NULL" else x for x in row]
            temp = [0 if x == "b0" else x for x in temp]
            temp = [1 if x == "b1" else x for x in temp]
            values.append(tuple(temp))

        # cursor.executemany(sql, values)

        for v in values:
            i = 0
            # for a in v:
            #     if a == "NULL":
            #         a = None
            if (table_name == "Listing"):
                for a in v:
                    print("###", xyz, columns[i], a)
                    i += 1
            xyz += 1
            cursor.execute(sql, v)

        db_connection.commit()
        print(table_name, cursor.rowcount, "record(s) inserted.")

        file.close()

    cursor.close()
