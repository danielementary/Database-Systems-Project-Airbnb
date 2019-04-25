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

        self.databaseConnection = None

        self.drawTop()
        self.drawTabs()

        self.connectDatabase()

        #search tab
        self.initialSearchFrameLabel = Label(self.searchFrame, text="Forms are available once connected to the DB.\n"
                                                                    "Please try 'Connect to DB' in 'Settings' tab.")
        self.initialSearchFrameLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        #queries tab
        Label(self.queriesFrame, text="This will be implemented later on.").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        #modifications tab
        Label(self.modificationsFrame, text="This will be implemented later on.").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        #settings tab
        Label(self.settingsFrame, text="These buttons are not needed if everything runs as expected.").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        Button(self.settingsFrame, text="Connect to DB",          command=self.connectDatabase)        .grid(row=1, column=0, sticky=W, padx=5, pady=5)
        Button(self.settingsFrame, text="Create and Populate DB", command=self.createAndPopulateTables).grid(row=2, column=0, sticky=W, padx=5, pady=5)
        Button(self.settingsFrame, text="Delete DB",              command=self.deleteDatabase)         .grid(row=3, column=0, sticky=W, padx=5, pady=5)

    def connectDatabase(self):
        if self.databaseConnection is None:
            self.databaseConnection = db.connect_database(DB_NAME)

            if self.databaseConnection is not None:
                self.statusLabel["text"] = "Connected to {} DB".format(DB_NAME)
                if (not db.has_tables(self.databaseConnection, DB_NAME)):
                    self.createAndPopulateTables()
                else:
                    self.tablesLabel["text"] = "Created"
                if (not db.every_table_has_entries(self.databaseConnection, DB_NAME)):
                    self.createAndPopulateTables()
                else:
                    self.dataLabel["text"] = "Loaded"
                    self.updateDatabaseVariables()
                    self.drawForms()
            else:
                self.statusLabel["text"] = "Please check that the MySQL server is running and configured"

    def createAndPopulateTables(self):
        db.execute_sql_list(self.databaseConnection, create_statements_ordered, "Tables creation")
        self.tablesLabel["text"] = "Created"
        db.populate_tables(self.databaseConnection, insert_tables_names_ordered, DATASET_PATH)
        self.dataLabel["text"] = "Loaded"
        self.updateDatabaseVariables()
        self.drawForms()

    def searchInDatabase(self):
        table = self.table.get()

        if (table == "Listing"):
            print(self.listingNameEntry.get(), self.accommodatesScale.get(),
                  self.squareFeetScale.get(), self.priceScale.get(),
                  self.isBusinessTravelReady.get(), self.reviewScoreRatingScale.get(),
                  self.propertyTypeIdDict[self.propertyTypeId.get()],
                  self.cancellationPolicyIdDict[self.cancellationPolicyId.get()])

        elif (table == "Host"):
            print(self.hostNameEntry.get())

        elif (table == "Neighbourhood"):
            print(self.NeighbourhoodNameEntry.get(), self.cityIdDict[self.cityId.get()])

    def updateSearchFields(self, value):
        if (self.previousTable != value):
            self.previousTable = value

            for i in range(1, 9):
                try:
                    self.searchFrame.grid_slaves(row=i, column=0)[0].grid_forget()
                    self.searchFrame.grid_slaves(row=i, column=1)[0].grid_forget()
                except:
                    #BAD !!!
                    break

            if (value == "Listing"):
                Label(self.searchFrame, text="Name").grid(row=1, column=0, sticky=W, padx=5, pady=5)
                self.listingNameEntry.grid(row=1, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Accommodates (min)").grid(row=2, column=0, sticky=W, padx=5, pady=5)
                self.accommodatesScale.grid(row=2, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Square Feet (min)").grid(row=3, column=0, sticky=W, padx=5, pady=5)
                self.squareFeetScale.grid(row=3, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Price (max)").grid(row=4, column=0, sticky=W, padx=5, pady=5)
                self.priceScale.grid(row=4, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Businness Travel Ready").grid(row=5, column=0, sticky=W, padx=5, pady=5)
                self.isBusinessTravelReadyCheckButton.grid(row=5, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Review Scores Rating (min)").grid(row=6, column=0, sticky=W, padx=5, pady=5)
                self.reviewScoreRatingScale.grid(row=6, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Property Type").grid(row=7, column=0, sticky=W, padx=5, pady=5)
                self.propertyTypeIdOptionMenu.grid(row=7, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Cancellation Policy").grid(row=8, column=0, sticky=W, padx=5, pady=5)
                self.cancellationPolicyIdOptionMenu.grid(row=8, column=1, sticky=W, padx=5, pady=5)

            elif (value == "Host"):
                Label(self.searchFrame, text="Name").grid(row=1, column=0, sticky=W, padx=5, pady=5)
                self.hostNameEntry.grid(row=1, column=1, sticky=W, padx=5, pady=5)

            elif (value == "Neighbourhood"):
                Label(self.searchFrame, text="Name").grid(row=1, column=0, sticky=W, padx=5, pady=5)
                self.NeighbourhoodNameEntry.grid(row=1, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="City").grid(row=2, column=0, sticky=W, padx=5, pady=5)
                self.cityIdOptionMenu.grid(row=2, column=1, sticky=W, padx=5, pady=5)

    def deleteDatabase(self):
        db.execute_sql(self.databaseConnection, "DROP DATABASE Airbnb;", "Airbnb drop")
        db.disconnect(self.databaseConnection)
        self.databaseConnection = None

    def drawTop(self):
        self.databaseSettingsFrame = ttk.Frame(self)
        self.databaseSettingsFrame.pack(fill=X)

        Label(self.databaseSettingsFrame, text="Status :").pack(side=LEFT, padx=5, pady=5)

        self.statusLabel = Label(self.databaseSettingsFrame, text="Not Connected")
        self.statusLabel.pack(side=LEFT, padx=5, pady=5)

        Label(self.databaseSettingsFrame, text="Tables :").pack(side=LEFT, padx=5, pady=5)

        self.tablesLabel = Label(self.databaseSettingsFrame, text="Not Created")
        self.tablesLabel.pack(side=LEFT, padx=5, pady=5)

        Label(self.databaseSettingsFrame, text="Data :").pack(side=LEFT, padx=5, pady=5)

        self.dataLabel = Label(self.databaseSettingsFrame, text="Not Loaded")
        self.dataLabel.pack(side=LEFT, padx=5, pady=5)

    def drawTabs(self):
        self.tabControl = ttk.Notebook(self)

        self.searchFrame        = ttk.Frame(self.tabControl)
        self.queriesFrame       = ttk.Frame(self.tabControl)
        self.modificationsFrame = ttk.Frame(self.tabControl)
        self.settingsFrame      = ttk.Frame(self.tabControl)

        self.tabControl.add(self.searchFrame,        text="Search")
        self.tabControl.add(self.queriesFrame,       text="Predefined Queries")
        self.tabControl.add(self.modificationsFrame, text="Insert/Delete")
        self.tabControl.add(self.settingsFrame,      text="Settings")

        self.tabControl.pack(fill=BOTH, expand=1)

    def drawForms(self):
        self.listingNameEntry  = Entry(self.searchFrame)

        self.accommodatesScale = Scale(self.searchFrame, from_=self.accommodatesMinMax[0],
                                                            to=self.accommodatesMinMax[1],
                                                        orient=HORIZONTAL)

        self.squareFeetScale   = Scale(self.searchFrame, from_=self.squareFeetMinMax[0],
                                                            to=self.squareFeetMinMax[1],
                                                        orient=HORIZONTAL)

        self.priceScale        = Scale(self.searchFrame, from_=self.priceMinMax[0],
                                                            to=self.priceMinMax[1],
                                                        orient=HORIZONTAL)

        self.isBusinessTravelReady = IntVar(self.searchFrame)
        self.isBusinessTravelReadyCheckButton = Checkbutton(self.searchFrame, variable=self.isBusinessTravelReady)

        self.reviewScoreRatingScale = Scale(self.searchFrame, from_=self.reviewScoresRatingMinMax[0],
                                                                 to=self.reviewScoresRatingMinMax[1],
                                                             orient=HORIZONTAL)

        self.propertyTypeId = StringVar(self.searchFrame)
        self.propertyTypeId.set(list(self.propertyTypeIdDict.keys())[0])
        self.propertyTypeIdOptionMenu = OptionMenu(self.searchFrame, self.propertyTypeId, *list(self.propertyTypeIdDict.keys()))

        self.cancellationPolicyId = StringVar(self.searchFrame)
        self.cancellationPolicyId.set(list(self.cancellationPolicyIdDict.keys())[0])
        self.cancellationPolicyIdOptionMenu = OptionMenu(self.searchFrame, self.cancellationPolicyId, *list(self.cancellationPolicyIdDict.keys()))

        #host
        self.hostNameEntry = Entry(self.searchFrame)

        #neighbourhood
        self.NeighbourhoodNameEntry = Entry(self.searchFrame)

        self.cityId = StringVar(self.searchFrame)
        self.cityId.set(list(self.cityIdDict.keys())[0])
        self.cityIdOptionMenu = OptionMenu(self.searchFrame, self.cityId, *list(self.cityIdDict.keys()))

        #label and option menu for table selection
        self.initialSearchFrameLabel.grid_forget()
        Label(self.searchFrame, text="Table").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.table = StringVar(self.searchFrame)
        temp = st.search_tables[0]
        self.table.set(temp)
        self.previousTable = None
        self.updateSearchFields(temp)
        self.tableOptionMenu = OptionMenu(self.searchFrame, self.table, *list(st.search_tables), command=self.updateSearchFields)
        self.tableOptionMenu.grid(row=0, column=1, padx=5, pady=5)

        self.searchButton = Button(self.searchFrame, text="Search", command=self.searchInDatabase)
        self.searchButton.grid(row=0, column=2, padx=5, pady=5)

    def updateDatabaseVariables(self):
        self.accommodatesMinMax       = self.getAccommodatesMinMax()
        self.squareFeetMinMax         = self.getSquareFeetMinMax()
        self.priceMinMax              = self.getPriceMinMax()
        self.reviewScoresRatingMinMax = self.getReviewScoresRatingMinMax()
        self.propertyTypeIdDict       = self.getPropertyTypeIdDict()
        self.cancellationPolicyIdDict = self.getCancellationPolicyIdDict()
        self.cityIdDict               = self.getCityIdDict()

    def getAccommodatesMinMax(self):
        return (0, 10)

    def getSquareFeetMinMax(self):
        return (0, 10)

    def getPriceMinMax(self):
        return (0, 10)

    def getReviewScoresRatingMinMax(self):
        return (0, 10)

    def getPropertyTypeIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection, st.select_property_type_names_ids_statements, "Select Property_type names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getCancellationPolicyIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection, st.select_cancellation_policy_names_ids_statements, "Select Cancellation_policy names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getCityIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection, st.select_city_names_ids_statements, "Select City names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result
