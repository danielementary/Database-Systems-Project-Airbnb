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
        self.protocol("WM_DELETE_WINDOW", self.disconnectAndClose)

        self.databaseConnection = None

        self.drawTop()
        self.drawTabs()

        self.initialSearchFrameLabel = Label(self.searchFrame, text="Forms are available once connected to the DB. Please try 'Connect to DB' in 'Settings' tab.")
        self.initialSearchFrameLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.initialQueriesFrameLabel = Label(self.queriesFrame, text="Predefined queries are available once connected to the DB. Please try 'Connect to DB' in 'Settings' tab.")
        self.initialQueriesFrameLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        Label(self.modificationsFrame, text="This will be implemented later on.").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        Label(self.settingsFrame, text="These buttons are not needed if everything runs as expected.").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        Button(self.settingsFrame, text="Connect to DB",          command=self.connectDatabase)        .grid(row=1, column=0, sticky=W, padx=5, pady=5)
        Button(self.settingsFrame, text="Create and Populate DB", command=self.createAndPopulateTables).grid(row=2, column=0, sticky=W, padx=5, pady=5)
        Button(self.settingsFrame, text="Delete DB",              command=self.deleteDatabase)         .grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.connectDatabase()

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
                    self.drawPredefinedQueries()
            else:
                self.statusLabel["text"] = "Please check that the MySQL server is running and configured"

    def disconnectAndClose(self):
        db.disconnect(self.databaseConnection)
        self.destroy()

    def createAndPopulateTables(self):
        db.execute_sql_list(self.databaseConnection, create_statements_ordered, "Tables creation")
        self.tablesLabel["text"] = "Created"
        db.populate_tables(self.databaseConnection, insert_tables_names_ordered, DATASET_PATH)
        self.dataLabel["text"] = "Loaded"
        self.updateDatabaseVariables()
        self.drawForms()
        self.drawPredefinedQueries()

    def searchInDatabase(self):
        table = self.table.get()

        if (table == "Listing"):
            values = tuple(["%"+self.listingNameEntry.get()+"%",
                            self.accommodatesScale.get(),
                            self.squareFeetScale.get(),
                            self.priceScale.get(),
                            self.isBusinessTravelReady.get(),
                            self.reviewScoreRatingScale.get(),
                            self.propertyTypeIdDict[self.propertyTypeId.get()],
                            self.cancellationPolicyIdDict[self.cancellationPolicyId.get()]])

            queryResults = db.select_sql_with_values(self.databaseConnection,
                                                     st.select_listing, values,
                                                     "Get listings")

            self.showResults(queryResults, st.select_listing, values)

        elif (table == "Host"):
            values = tuple(["%"+self.hostNameEntry.get()+"%"])

            queryResults = db.select_sql_with_values(self.databaseConnection,
                                                     st.select_host, values,
                                                     "Get hosts")

            self.showResults(queryResults, st.select_host, values)

        elif (table == "Neighbourhood"):
            values = tuple(["%"+self.NeighbourhoodNameEntry.get()+"%",
                            self.cityIdDict[self.cityId.get()]])

            queryResults = db.select_sql_with_values(self.databaseConnection,
                                                     st.select_neighbourhood, values,
                                                     "Get neighbourhoods")

            self.showResults(queryResults, st.select_neighbourhood, values)

    def executePredefinedQuery(self):
        sql = st.predefined_queries[self.predefniedQuery.get()]

        queryResults = db.select_sql(self.databaseConnection, sql, "Execute predefined query")

        self.showResults(queryResults, sql, None)

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
                self.accommodatesScale.set(self.accommodatesMinMax[0])

                Label(self.searchFrame, text="Square Feet (min)").grid(row=3, column=0, sticky=W, padx=5, pady=5)
                self.squareFeetScale.grid(row=3, column=1, sticky=W, padx=5, pady=5)
                self.squareFeetScale.set(self.squareFeetMinMax[0])

                Label(self.searchFrame, text="Price (max)").grid(row=4, column=0, sticky=W, padx=5, pady=5)
                self.priceScale.grid(row=4, column=1, sticky=W, padx=5, pady=5)
                self.priceScale.set(self.priceMinMax[1])

                Label(self.searchFrame, text="Businness Travel Ready").grid(row=5, column=0, sticky=W, padx=5, pady=5)
                self.isBusinessTravelReadyCheckButton.grid(row=5, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Review Scores Rating (min)").grid(row=6, column=0, sticky=W, padx=5, pady=5)
                self.reviewScoreRatingScale.grid(row=6, column=1, sticky=W, padx=5, pady=5)
                self.reviewScoreRatingScale.set(self.reviewScoresRatingMinMax[0])

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
                                                        orient=HORIZONTAL,
                                                        length=160)

        self.squareFeetScale   = Scale(self.searchFrame, from_=self.squareFeetMinMax[0],
                                                            to=self.squareFeetMinMax[1],
                                                        orient=HORIZONTAL,
                                                        length=160)

        self.priceScale        = Scale(self.searchFrame, from_=self.priceMinMax[0],
                                                            to=self.priceMinMax[1],
                                                        orient=HORIZONTAL,
                                                        length=160)

        self.isBusinessTravelReady = IntVar(self.searchFrame)
        self.isBusinessTravelReadyCheckButton = Checkbutton(self.searchFrame, variable=self.isBusinessTravelReady)

        self.reviewScoreRatingScale = Scale(self.searchFrame, from_=self.reviewScoresRatingMinMax[0],
                                                                 to=self.reviewScoresRatingMinMax[1],
                                                             orient=HORIZONTAL,
                                                             length=160)

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
        try:
            result = db.select_sql(self.databaseConnection,
                          st.select_listing_accomodates_min_max,
                          "Select Listing accommodates min and max")[0]
        except:
            result = (0, 0)
        finally:
            return result

    def getSquareFeetMinMax(self):
        try:
            result = db.select_sql(self.databaseConnection,
                          st.select_listing_sqare_feet_min_max,
                          "Select Listing square_feet min and max")[0]
        except:
            result = (0, 0)
        finally:
            return result

    def getPriceMinMax(self):
        try:
            result = db.select_sql(self.databaseConnection,
                          st.select_listing_price_min_max,
                          "Select Listing price min and max")[0]
        except:
            result = (0, 0)
        finally:
            return result

    def getReviewScoresRatingMinMax(self):
        try:
            result = db.select_sql(self.databaseConnection,
                          st.select_listing_review_score_rating_min_max,
                          "Select Listing review_scores_rating min and max")[0]
        except:
            result = (0, 0)
        finally:
            return result

    def getPropertyTypeIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                          st.select_property_type_names_ids_statements,
                          "Select Property_type names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getCancellationPolicyIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                          st.select_cancellation_policy_names_ids_statements,
                          "Select Cancellation_policy names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getCityIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                          st.select_city_names_ids_statements,
                          "Select City names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def drawPredefinedQueries(self):
        self.initialQueriesFrameLabel.grid_forget()
        Label(self.queriesFrame, text="Query").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.predefniedQuery = StringVar(self.queriesFrame)
        self.predefniedQuery.set(list(st.predefined_queries.keys())[0])
        self.predefniedQueryOptionMenu = OptionMenu(self.queriesFrame, self.predefniedQuery, *list(st.predefined_queries.keys()))
        self.predefniedQueryOptionMenu.grid(row=0, column=1, sticky=W, padx=5, pady=5)

        self.executeButton = Button(self.queriesFrame, text="Execute", command=self.executePredefinedQuery)
        self.executeButton.grid(row=0, column=2, padx=5, pady=5)

    def showResults(self, queryResults, sql, values):
        Results(self, queryResults, sql, values).focus()

class Results(Toplevel):
    def __init__(self, master, queryResults, sql, values, **options):
        Toplevel.__init__(self, master, **options)
        self.title("DBS-Project Group32 Results")
        self.geometry("1280x720")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.closeResults)

        self.master.searchButton["state"]  =  DISABLED
        self.master.executeButton["state"] =  DISABLED

        sql = " ".join(sql.replace("\n", " ").split()).replace(",", ",\n").replace("and", "and\n")

        Label(self, text="Please close this windows before next operations.").grid(row=0, column=0, sticky=W, padx=5, pady=5, columnspan=2)

        Label(self, text="MySQL Statement").grid(row=1, column=0, sticky=N, padx=5, pady=5)
        Label(self, text="Values").grid(row=1, column=1, sticky=N, padx=5, pady=5)

        Label(self, text=sql)   .grid(row=2, column=0, sticky=NW, padx=5, pady=5)
        Label(self, text=values).grid(row=2, column=1, sticky=NW, padx=5, pady=5)

        Label(self, text="Results ({})".format(len(queryResults))).grid(row=3, column=0, sticky=N, padx=5, pady=5, columnspan=2)

        i = 4
        for r in queryResults:
            Label(self, text=r).grid(row=i, column=0, sticky=NW, padx=5, pady=5, columnspan=2)
            i += 1

    def closeResults(self):
        self.master.searchButton["state"]  = NORMAL
        self.master.executeButton["state"] = NORMAL
        self.destroy()
