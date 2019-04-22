from tkinter import *
from tkinter import ttk

import os

import src.database as db
import database.select_tables as st

from database.create_tables import create_statements_ordered
from database.insert_tables import insert_tables_names_ordered

DB_NAME = "Airbnb"
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Dataset/Final/")

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.title("DBS-Project Group32")
        self.geometry("1280x720")
        self.resizable(width=False, height=False)

        #database variables
        self.databaseConnection           = None

        self.accommodates_min_max         = None
        self.square_feet_min_max          = None
        self.price_min_max                = None
        self.review_scores_rating_min_max = None
        self.property_type_id_list        = None
        self.cancellation_policy_id_list  = None
        self.host_since_oldest            = None
        self.city_id_list                 = None

        #top frame for connection status
        self.databaseSettingsFrame = ttk.Frame(self)
        self.databaseSettingsFrame.pack(fill=X)

        Label(self.databaseSettingsFrame, text="Status").pack(side=LEFT, padx=5, pady=5)

        self.statusLabel = Label(self.databaseSettingsFrame, text="Not Connected")
        self.statusLabel.pack(side=LEFT, padx=5, pady=5)

        self.connectionButton = Button(self.databaseSettingsFrame, text="Try again", command=self.connectDatabase)

        Button(self.databaseSettingsFrame, text="Delete DB", command=self.deleteDatabase).pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)
        Button(self.databaseSettingsFrame, text="Connect DB", command=self.connectDatabase).pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)
        Button(self.databaseSettingsFrame, text="Populate DB", command=self.populateDatabase).pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)

        #tabs and conresponding frames
        self.tabControl = ttk.Notebook(self)

        self.searchFrame        = ttk.Frame(self.tabControl)
        self.queriesFrame       = ttk.Frame(self.tabControl)
        self.modificationsFrame = ttk.Frame(self.tabControl)

        self.tabControl.add(self.searchFrame,        text="Search")
        self.tabControl.add(self.queriesFrame,       text="Predefined Queries")
        self.tabControl.add(self.modificationsFrame, text="Insert/Delete")

        self.tabControl.pack(fill=BOTH, expand=1)

        #search tab
        #table label
        Label(self.searchFrame, text="Table").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        #option menu for table selection
        self.table = StringVar(self.searchFrame)
        temp = list(st.search_fields.keys())[0]
        self.table.set(temp)
        self.previousTable = None
        self.updateSearchFields(temp)
        self.tableOptionMenu = OptionMenu(self.searchFrame, self.table, *list(st.search_fields.keys()), command=self.updateSearchFields)
        self.tableOptionMenu.grid(row=0, column=1, padx=5, pady=5)

        #queries tab
        Label(self.queriesFrame, text="This will be implemented later on.").pack()

        #modifications tab
        Label(self.modificationsFrame, text="This will be implemented later on.").pack()
        self.connectDatabase()

    def connectDatabase(self):
        if self.databaseConnection is None:
            self.databaseConnection = db.connect_database(DB_NAME)

            if self.databaseConnection is not None:
                self.statusLabel["text"] = "Connected to {} DB".format(DB_NAME)
                self.connectionButton.pack_forget()
                if (db.count_tables(self.databaseConnection, DB_NAME) <= 0):
                    self.createTables()
            else:
                self.statusLabel["text"] = "Please check that the MySQL server is running and configured"
                self.connectionButton.pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)

    def createTables(self):
        db.execute_sql_list(self.databaseConnection, create_statements_ordered, "Tables creation")
        # db.populate_tables(self.databaseConnection, insert_tables_names_ordered, DATASET_PATH)

    def updateSearchFields(self, value):
        if (self.previousTable != value):
            self.previousTable = value
            searchFieldList = st.search_fields[value]

            for i in range(1, 11):
                try:
                    self.searchFrame.grid_slaves(row=i, column=0)[0].grid_forget()
                    self.searchFrame.grid_slaves(row=i, column=1)[0].grid_forget()
                except:
                    #BAD !!!
                    break

            rowForm = 1
            for sf in searchFieldList:
                Label(self.searchFrame, text=sf).grid(row=rowForm, column=0, sticky=W, padx=5, pady=5)

                input = Entry(self.searchFrame)

                input.grid(row=rowForm, column=1, sticky=W, padx=5, pady=5)
                rowForm += 1

    def deleteDatabase(self):
        db.execute_sql(self.databaseConnection, "DROP DATABASE Airbnb;", "Airbnb drop")
        db.disconnect(self.databaseConnection)
        self.databaseConnection = None

    def populateDatabase(self):
        db.populate_tables(self.databaseConnection, insert_tables_names_ordered, DATASET_PATH)
