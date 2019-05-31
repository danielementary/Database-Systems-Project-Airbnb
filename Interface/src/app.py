from tkinter import *
from tkinter import ttk

import os

from src.results import Results

import src.database as db
import database.select_tables as st

from database.create_tables import create_statements_ordered
from database.insert_tables import insert_tables_names_ordered

from database.create_indexes import create_indexes as create_indexes_list
from database.drop_indexes   import drop_indexes   as drop_indexes_list

DB_NAME = "Airbnb"
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Datasets/Final/")

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.title("DBS-Project Group32")
        self.geometry("1400x800")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.disconnectAndClose)

        self.databaseConnection = None

        self.drawTop()
        self.drawTabs()
        self.drawWidgets()

        self.connectDatabase()

    def connectDatabase(self):
        if self.databaseConnection is None:
            self.databaseConnection = db.connect_database(DB_NAME)

            if self.databaseConnection is not None:
                self.statusLabel["text"] = "Connected to {} DB".format(DB_NAME)
                if (not db.has_tables(self.databaseConnection, len(create_statements_ordered), DB_NAME) or
                    not db.every_table_has_entries(self.databaseConnection, DB_NAME)):
                    try:
                        self.createAndPopulateTables()
                    except:
                        self.deleteDatabase()
                        self.connectDatabase()
                else:
                    self.tablesLabel["text"] = "Created"
                    self.dataLabel["text"] = "Loaded"
                    self.updateDatabaseVariables()
                    self.drawForms()
                    self.drawDelete()
                    self.drawPredefinedQueries()
                    self.drawInsert()
            else:
                self.statusLabel["text"] = "Please check that the MySQL server is running and configured"

    def disconnectAndClose(self):
        self.drop_indexes()
        db.disconnect(self.databaseConnection)
        self.destroy()

    def createAndPopulateTables(self):
        db.execute_sql_list(self.databaseConnection, create_statements_ordered, "Tables creation")
        self.tablesLabel["text"] = "Created"
        db.populate_tables(self.databaseConnection, insert_tables_names_ordered, DATASET_PATH)
        self.dataLabel["text"] = "Loaded"
        self.updateDatabaseVariables()
        self.drawForms()
        self.drawDelete()
        self.drawPredefinedQueries()

    def searchInDatabase(self):
        table = self.table.get()

        if (table == "Listing"):
            values = tuple(["%"+self.listingNameEntry.get()+"%",
                            self.accommodatesScale.get(),
                            self.squareFeetScale.get(),
                            self.priceScale.get(),
                            self.isBusinessTravelReady.get(),
                            self.cityIdDict[self.searchListingCityId.get()],
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

    def insertListingInDatabase(self):
        values  = []

        id = db.select_sql(self.databaseConnection, "SELECT MAX(listing_id) FROM Listing", "Select biggest listing_id")[0][0] + 1
        values.append("{}".format(id))

        tempName = self.insertListingNameEntry.get()[:250]
        if (len(tempName) <= 0):
            values.append("id : {}".format(id))
        else:
            values.append(tempName)

        tempSummary = self.insertListingSummaryEntry.get()[:65000]
        if (len(tempSummary) <= 0):
            values.append("There is no summary for this listing.")
        else:
            values.append(tempSummary)

        values.append(self.insertListingAccomodatesScale.get())
        values.append(self.insertListingSquareFeetScale.get())
        values.append(self.insertListingPriceScale.get())
        values.append(self.listingHostId)
        values.append(self.listingNeighbourhoodId)
        values.append(self.insertListingIsBusinessTravelReady.get())
        values.append(self.propertyTypeIdDict[self.insertListingPropertyTypeId.get()])
        values.append(self.roomTypeIdDict[self.insertListingRoomTypeId.get()])
        values.append(self.bedTypeIdDict[self.insertListingBedTypeId.get()])
        values.append(self.cancellationPolicyIdDict[self.insertListingCancellationPolicyId.get()])

        db.insert_listing(self.databaseConnection, values)
        self.updateDatabaseVariables()
        self.insertFrame.grid_slaves(row=5, column=8)[0].grid_forget()
        self.insertFrame.grid_slaves(row=6, column=8)[0].grid_forget()
        self.drawInsert()

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
                self.listingNameEntry               .grid(row=1, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Accommodates (min)").grid(row=2, column=0, sticky=W, padx=5, pady=5)
                self.accommodatesScale                            .grid(row=2, column=1, sticky=W, padx=5, pady=5)
                self.accommodatesScale.set(self.accommodatesMinMax[0])

                Label(self.searchFrame, text="Square Feet (min)").grid(row=3, column=0, sticky=W, padx=5, pady=5)
                self.squareFeetScale                             .grid(row=3, column=1, sticky=W, padx=5, pady=5)
                self.squareFeetScale.set(self.squareFeetMinMax[0])

                Label(self.searchFrame, text="Price (max)").grid(row=4, column=0, sticky=W, padx=5, pady=5)
                self.priceScale                            .grid(row=4, column=1, sticky=W, padx=5, pady=5)
                self.priceScale.set(self.priceMinMax[1])

                Label(self.searchFrame, text="City").grid(row=5, column=0, sticky=W, padx=5, pady=5)
                self.searchListingCityIdOptionMenu  .grid(row=5, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Businness Travel Ready").grid(row=6, column=0, sticky=W, padx=5, pady=5)
                self.isBusinessTravelReadyCheckButton                 .grid(row=6, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Property Type").grid(row=7, column=0, sticky=W, padx=5, pady=5)
                self.propertyTypeIdOptionMenu                .grid(row=7, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="Cancellation Policy").grid(row=8, column=0, sticky=W, padx=5, pady=5)
                self.cancellationPolicyIdOptionMenu                .grid(row=8, column=1, sticky=W, padx=5, pady=5)

            elif (value == "Host"):
                Label(self.searchFrame, text="Name").grid(row=1, column=0, sticky=W, padx=5, pady=5)
                self.hostNameEntry                  .grid(row=1, column=1, sticky=W, padx=5, pady=5)

            elif (value == "Neighbourhood"):
                Label(self.searchFrame, text="Name").grid(row=1, column=0, sticky=W, padx=5, pady=5)
                self.NeighbourhoodNameEntry         .grid(row=1, column=1, sticky=W, padx=5, pady=5)

                Label(self.searchFrame, text="City").grid(row=2, column=0, sticky=W, padx=5, pady=5)
                self.cityIdOptionMenu               .grid(row=2, column=1, sticky=W, padx=5, pady=5)

    def deleteDatabase(self):
        for w in self.winfo_children():
            w.destroy()
        db.execute_sql(self.databaseConnection, "DROP DATABASE Airbnb;", "Airbnb drop")
        db.disconnect(self.databaseConnection)
        self.databaseConnection = None
        self.drawTop()
        self.drawTabs()
        self.drawWidgets()

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

        self.topIndex = Label(self.databaseSettingsFrame, text="Indexes are not actived")
        self.topIndex.pack(side=LEFT, padx=5, pady=5)

    def drawTabs(self):
        self.tabControl = ttk.Notebook(self)

        self.searchFrame   = ttk.Frame(self.tabControl)
        self.queriesFrame  = ttk.Frame(self.tabControl)
        self.insertFrame   = ttk.Frame(self.tabControl)
        self.deleteFrame   = ttk.Frame(self.tabControl)
        self.settingsFrame = ttk.Frame(self.tabControl)

        self.tabControl.add(self.searchFrame,   text="Search")
        self.tabControl.add(self.insertFrame,   text="Insert A Listing")
        self.tabControl.add(self.queriesFrame,  text="Predefined Queries")
        self.tabControl.add(self.deleteFrame,   text="Delete")
        self.tabControl.add(self.settingsFrame, text="Settings")

        self.tabControl.pack(fill=BOTH, expand=1)

    def drawWidgets(self):
        self.initialSearchFrameLabel = Label(self.searchFrame, text="Forms are available once connected to the DB. Please try 'Connect to DB' in 'Settings' tab.")
        self.initialSearchFrameLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.initialQueriesFrameLabel = Label(self.queriesFrame, text="Predefined queries are available once connected to the DB. Please try 'Connect to DB' in 'Settings' tab.")
        self.initialQueriesFrameLabel.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        Label( self.settingsFrame, text="These buttons are not needed if everything runs as expected.").grid(row=0, column=0, sticky=W, padx=5, pady=5, columnspan=2)

        self.connectDatabaseButton = Button(self.settingsFrame, text="Connect to DB", command=self.connectDatabase)
        self.deleteDatabaseButton  = Button(self.settingsFrame, text="Delete DB",     command=self.deleteDatabase)

        self.connectDatabaseButton.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.deleteDatabaseButton .grid(row=1, column=1, sticky=W, padx=5, pady=5)

        self.createIndexesButton = Button(self.settingsFrame, text="Create Indexes", command=self.create_indexes)
        self.dropIndexesButton   = Button(self.settingsFrame, text="Drop Indexes",   command=self.drop_indexes)

        self.createIndexesButton.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.dropIndexesButton  .grid(row=2, column=1, sticky=W, padx=5, pady=5)

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
        self.isBusinessTravelReadyCheckButton = Checkbutton(self.searchFrame,
                                                            variable=self.isBusinessTravelReady)

        self.searchListingCityId = StringVar(self.searchFrame)
        self.searchListingCityId.set(list(self.cityIdDict.keys())[0])
        self.searchListingCityIdOptionMenu = OptionMenu(self.searchFrame,
                                                   self.searchListingCityId,
                                                   *list(self.cityIdDict.keys()))

        self.propertyTypeId = StringVar(self.searchFrame)
        self.propertyTypeId.set(list(self.propertyTypeIdDict.keys())[0])
        self.propertyTypeIdOptionMenu = OptionMenu(self.searchFrame,
                                                   self.propertyTypeId,
                                                   *list(self.propertyTypeIdDict.keys()))

        self.cancellationPolicyId = StringVar(self.searchFrame)
        self.cancellationPolicyId.set(list(self.cancellationPolicyIdDict.keys())[0])
        self.cancellationPolicyIdOptionMenu = OptionMenu(self.searchFrame,
                                                         self.cancellationPolicyId,
                                                         *list(self.cancellationPolicyIdDict.keys()))

        #host
        self.hostNameEntry = Entry(self.searchFrame)

        #neighbourhood
        self.NeighbourhoodNameEntry = Entry(self.searchFrame)

        self.cityId = StringVar(self.searchFrame)
        self.cityId.set(list(self.cityIdDict.keys())[0])
        self.cityIdOptionMenu = OptionMenu(self.searchFrame,
                                           self.cityId,
                                           *list(self.cityIdDict.keys()))

        #label and option menu for table selection
        self.initialSearchFrameLabel.grid_forget()
        Label(self.searchFrame, text="Table").grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.table = StringVar(self.searchFrame)
        temp = st.search_tables[0]
        self.table.set(temp)
        self.previousTable = None
        self.updateSearchFields(temp)
        self.tableOptionMenu = OptionMenu(self.searchFrame,
                                          self.table,
                                          *list(st.search_tables), command=self.updateSearchFields)
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
        self.roomTypeIdDict           = self.getRoomTypeIdDict()
        self.bedTypeIdDict            = self.getBedTypeIdDict()
        self.neighbourhoodIdDict      = self.getNeighbourhoodIdDict()

    def updateHostNeighboorhoods(self, cityName):
        self.neighbourhoodIdDict = self.getNeighbourhoodIdForCityIdDict(self.cityIdDict[cityName])
        self.insertListingHostNeighboorhoodOptionMenu.grid_forget()
        self.insertListingHostNeighboorhood = StringVar(self.insertFrame)
        self.insertListingHostNeighboorhood.set(list(self.neighbourhoodIdDict.keys())[0])
        self.insertListingHostNeighboorhoodOptionMenu = OptionMenu(self.insertFrame,
                                                            self.insertListingHostNeighboorhood,
                                                            *list(self.neighbourhoodIdDict.keys()))
        self.insertListingHostNeighboorhoodOptionMenu.grid(row=5, column=4, sticky=W, padx=5, pady=5)

    def checkHost(self):
        if (len(self.insertListingHost.get()) > 0):
            self.insertListingCheckHostButton["state"] = DISABLED
            if (self.insertListingCheckNeighboorhoodButton["state"] == DISABLED):
                self.insertButton["state"] = NORMAL

            values = (self.insertListingHost.get(),
                      self.neighbourhoodIdDict[self.insertListingHostNeighboorhood.get()])

            result = db.select_sql_with_values(self.databaseConnection,
                                               st.find_host, (values),
                                               "Check Host")
            if (len(result) == 1):
                self.listingHostId = result[0][0]
            else:
                self.listingHostId = db.select_sql(self.databaseConnection, "SELECT MAX(host_id) FROM Host", "Select biggest host_id")[0][0] + 1
                values = [self.listingHostId, self.insertListingHost.get(), self.neighbourhoodIdDict[self.insertListingHostNeighboorhood.get()]]
                db.insert_host(self.databaseConnection, values)

            Label(self.insertFrame, text="id : {}".format(self.listingHostId)).grid(row=5, column=8, sticky=W, padx=5, pady=5)

    def checkNeighboorhood(self):
        if (len(self.insertListingNeighbourhood.get()) > 0):
            self.insertListingCheckNeighboorhoodButton["state"] = DISABLED
            if (self.insertListingCheckHostButton["state"] == DISABLED):
                self.insertButton["state"] = NORMAL

            values = (self.insertListingNeighbourhood.get(),
                      self.cityIdDict[self.insertListingNeighbourhoodCity.get()])

            result = db.select_sql_with_values(self.databaseConnection,
                                               st.find_neighbourhood, (values),
                                               "Check Neighbourhood")
            if (len(result) == 1):
                self.listingNeighbourhoodId = result[0][0]
            else:
                self.listingNeighbourhoodId = db.select_sql(self.databaseConnection, "SELECT MAX(neighbourhood_id) FROM Neighbourhood", "Select biggest neighbourhood_id")[0][0] + 1
                values = [self.listingNeighbourhoodId, self.insertListingNeighbourhood.get(), self.cityIdDict[self.insertListingNeighbourhoodCity.get()]]
                db.insert_neighboorhood(self.databaseConnection, values)

            Label(self.insertFrame, text="id : {}".format(self.listingNeighbourhoodId)).grid(row=6, column=8, sticky=W, padx=5, pady=5)

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

    def getRoomTypeIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                                        st.select_room_type_names_ids_statements,
                                        "Select Room_type names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getBedTypeIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                                        st.select_bed_type_names_ids_statements,
                                        "Select Bed_type names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getNeighbourhoodIdDict(self):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                                        st.select_neighbourhood_names_ids_statements,
                                        "Select Neighbourhood names and ids"))
        except:
            result = {"None": 0}
        finally:
            return result

    def getNeighbourhoodIdForCityIdDict(self, cityId):
        try:
            result = dict(db.select_sql(self.databaseConnection,
                                        st.select_neighbourhood_names_ids_for_city_id_statements.format(cityId),
                                        "Select Neighbourhood names and ids for city {}".format(cityId)))
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

    def drawInsert(self):
        self.insertListingNameEntry = Entry(self.insertFrame)
        Label(self.insertFrame, text="Name").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.insertListingNameEntry              .grid(row=0, column=1, sticky=W, padx=5, pady=5)

        self.insertListingSummaryEntry = Entry(self.insertFrame)
        Label(self.insertFrame, text="Summary").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.insertListingSummaryEntry              .grid(row=1, column=1, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Accommodates").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.insertListingAccomodatesScale = Scale(self.insertFrame, from_=0,
                                                                        to=self.accommodatesMinMax[1]*2,
                                                                    orient=HORIZONTAL,
                                                                    length=160)
        self.insertListingAccomodatesScale.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        self.insertListingAccomodatesScale.set(0)

        Label(self.insertFrame, text="Square Feet").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.insertListingSquareFeetScale = Scale(self.insertFrame, from_=0,
                                                                       to=self.squareFeetMinMax[1]*2,
                                                                   orient=HORIZONTAL,
                                                                   length=160)
        self.insertListingSquareFeetScale.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        self.insertListingSquareFeetScale.set(0)

        Label(self.insertFrame, text="Price").grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.insertListingPriceScale = Scale(self.insertFrame, from_=0,
                                                                  to=self.priceMinMax[1]*2,
                                                              orient=HORIZONTAL,
                                                              length=160)
        self.insertListingPriceScale.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        self.insertListingPriceScale.set(0)

        self.insertListingHost = Entry(self.insertFrame)
        Label(self.insertFrame, text="Host : ").grid(row=5, column=0, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="City").grid(row=5, column=1, sticky=W, padx=5, pady=5)
        self.insertListingHostCity = StringVar(self.insertFrame)
        self.insertListingHostCity.set(list(self.cityIdDict.keys())[0])
        self.insertListingHostCityOptionMenu = OptionMenu(self.insertFrame,
                                                          self.insertListingHostCity,
                                                          *list(self.cityIdDict.keys()),
                                                          command=self.updateHostNeighboorhoods)
        self.insertListingHostCityOptionMenu.grid(row=5, column=2, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Neighbourhood").grid(row=5, column=3, sticky=W, padx=5, pady=5)
        self.insertListingHostNeighboorhood = StringVar(self.insertFrame)
        self.insertListingHostNeighboorhood.set(list(self.neighbourhoodIdDict.keys())[0])
        self.insertListingHostNeighboorhoodOptionMenu = OptionMenu(self.insertFrame,
                                                            self.insertListingHostNeighboorhood,
                                                            *list(self.neighbourhoodIdDict.keys()))
        self.insertListingHostNeighboorhoodOptionMenu.grid(row=5, column=4, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Name").grid(row=5, column=5, sticky=W, padx=5, pady=5)
        self.insertListingHost              .grid(row=5, column=6, sticky=W, padx=5, pady=5)

        self.insertListingCheckHostButton = Button(self.insertFrame, text="Check Host", command=self.checkHost)
        self.insertListingCheckHostButton.grid(row=5, column=7, padx=5, pady=5)

        self.insertListingNeighbourhood = Entry(self.insertFrame)
        Label(self.insertFrame, text="Neighbourhood : ").grid(row=6, column=0, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="City").grid(row=6, column=1, sticky=W, padx=5, pady=5)
        self.insertListingNeighbourhoodCity = StringVar(self.insertFrame)
        self.insertListingNeighbourhoodCity.set(list(self.cityIdDict.keys())[0])
        self.insertListingNeighbourhoodCityOptionMenu = OptionMenu(self.insertFrame,
                                                          self.insertListingNeighbourhoodCity,
                                                          *list(self.cityIdDict.keys()))
        self.insertListingNeighbourhoodCityOptionMenu.grid(row=6, column=2, sticky=W, padx=5, pady=5)
        Label(self.insertFrame, text="Name").grid(row=6, column=5, sticky=W, padx=5, pady=5)
        self.insertListingNeighbourhood     .grid(row=6, column=6, sticky=W, padx=5, pady=5)

        self.insertListingCheckNeighboorhoodButton = Button(self.insertFrame, text="Check Neighbourhood", command=self.checkNeighboorhood)
        self.insertListingCheckNeighboorhoodButton.grid(row=6, column=7, padx=5, pady=5)

        Label(self.insertFrame, text="Businness Travel Ready").grid(row=7, column=0, sticky=W, padx=5, pady=5)
        self.insertListingIsBusinessTravelReady = IntVar(self.insertFrame)
        self.insertListingIsBusinessTravelReadyCheckButton = Checkbutton(self.insertFrame,
                                                                         variable=self.insertListingIsBusinessTravelReady)
        self.insertListingIsBusinessTravelReadyCheckButton.grid(row=7, column=2, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Property Type").grid(row=8, column=0, sticky=W, padx=5, pady=5)
        self.insertListingPropertyTypeId = StringVar(self.insertFrame)
        self.insertListingPropertyTypeId.set(list(self.propertyTypeIdDict.keys())[0])
        self.insertListingPropertyTypeIdOptionMenu = OptionMenu(self.insertFrame,
                                                                self.insertListingPropertyTypeId,
                                                                *list(self.propertyTypeIdDict.keys()))
        self.insertListingPropertyTypeIdOptionMenu.grid(row=8, column=1, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Room Type").grid(row=9, column=0, sticky=W, padx=5, pady=5)
        self.insertListingRoomTypeId = StringVar(self.insertFrame)
        self.insertListingRoomTypeId.set(list(self.roomTypeIdDict.keys())[0])
        self.insertListingRoomTypeIdOptionMenu = OptionMenu(self.insertFrame,
                                                            self.insertListingRoomTypeId,
                                                            *list(self.roomTypeIdDict.keys()))
        self.insertListingRoomTypeIdOptionMenu.grid(row=9, column=1, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Bed Type").grid(row=10, column=0, sticky=W, padx=5, pady=5)
        self.insertListingBedTypeId = StringVar(self.insertFrame)
        self.insertListingBedTypeId.set(list(self.bedTypeIdDict.keys())[0])
        self.insertListingBedTypeIdOptionMenu = OptionMenu(self.insertFrame,
                                                           self.insertListingBedTypeId,
                                                           *list(self.bedTypeIdDict.keys()))
        self.insertListingBedTypeIdOptionMenu.grid(row=10, column=1, sticky=W, padx=5, pady=5)

        Label(self.insertFrame, text="Cancellation Policy").grid(row=11, column=0, sticky=W, padx=5, pady=5)
        self.insertListingCancellationPolicyId = StringVar(self.insertFrame)
        self.insertListingCancellationPolicyId.set(list(self.cancellationPolicyIdDict.keys())[0])
        self.insertListingCancellationPolicyIdOptionMenu = OptionMenu(self.insertFrame,
                                                                      self.insertListingCancellationPolicyId,
                                                                      *list(self.cancellationPolicyIdDict.keys()))
        self.insertListingCancellationPolicyIdOptionMenu.grid(row=11, column=1, sticky=W, padx=5, pady=5)


        self.insertButton = Button(self.insertFrame, text="Insert", command=self.insertListingInDatabase)
        self.insertButton.grid(row=0, column=8, padx=5, pady=5)
        self.insertButton["state"] = DISABLED
        Label(self.insertFrame, text="Please check host and neighbourhood before inserting the listing.").grid(row=0, column=3, sticky=W, padx=5, pady=5, columnspan=5)

    def drawDelete(self):
        self.deleteTable = StringVar(self.deleteFrame)
        self.deleteTable.set(st.delete_tables[0])
        self.deleteTableOptionMenu = OptionMenu(self.deleteFrame,
                                                self.deleteTable,
                                                *list(st.delete_tables))
        self.deleteTableOptionMenu.grid(row=0, column=0, padx=5, pady=5)

        Label(self.deleteFrame, text="id").grid(row=0, column=1, padx=5, pady=5)

        self.deleteIdEntry = Entry(self.deleteFrame)
        self.deleteIdEntry.grid(row=0, column=2, sticky=W, padx=5, pady=5)

        Button(self.deleteFrame, text="delete", command=self.deleteFromDatabase).grid(row=0, column=3, padx=5, pady=5)

    def deleteFromDatabase(self):
        sql = "DELETE FROM {} WHERE {} = {}".format(self.deleteTable.get(), st.id_map[self.deleteTable.get()], self.deleteIdEntry.get())
        db.execute_sql(self.databaseConnection, sql, "Delete by id")

    def create_indexes(self):
        self.topIndex["text"] = "Indexes are now actived"
        db.execute_sql_list(self.databaseConnection, create_indexes_list, "Create indexes")

    def drop_indexes(self):
        self.topIndex["text"] = "Indexes are not actived"
        db.execute_sql_list(self.databaseConnection, drop_indexes_list, "Drop indexes")

    def showResults(self, queryResults, sql, values):
        Results(self, queryResults, sql, values).focus()
