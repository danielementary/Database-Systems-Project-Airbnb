from tkinter import *
from tkinter import ttk

import src.database as db

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.title("DBS-Project Group32")
        self.geometry("1280x720")
        self.resizable(width=False, height=False)
        self.databaseConnection = None

        databaseSettingsFrame = ttk.Frame(self)
        databaseSettingsFrame.pack(fill=X)

        Label(databaseSettingsFrame, text="Status").pack(side=LEFT, padx=5, pady=5)

        statusLabel = Label(databaseSettingsFrame, text="Not Connected")
        statusLabel.pack(side=LEFT, padx=5, pady=5)

        connectionButton = Button(databaseSettingsFrame, text="Connect to Airbnb DB", command=lambda : connectDatabase(self))
        connectionButton.pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)

        tabControl = ttk.Notebook(self)

        searchFrame        = ttk.Frame(tabControl)
        queriesFrame       = ttk.Frame(tabControl)
        modificationsFrame = ttk.Frame(tabControl)

        tabControl.add(searchFrame,        text="Search")
        tabControl.add(queriesFrame,       text="Predefined Queries")
        tabControl.add(modificationsFrame, text="Insert/Delete")

        tabControl.pack(fill=BOTH, expand=1)

        #search tab
        #search label
        Label(searchFrame, text="Search Box").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        #search search box
        searchBox = Entry(searchFrame)
        searchBox.grid(row=0, column=1, padx=5, pady=5)
        #search button
        searchButton = Button(searchFrame, text="Search", state=DISABLED)
        searchButton.grid(row=0, column=2, padx=5, pady=5)

        #queries tab
        Label(queriesFrame, text="This will be implemented later on.").pack()

        #modifications tab
        Label(modificationsFrame, text="This will be implemented later on.").pack()

        def connectDatabase(self):
            if self.databaseConnection is None:
                self.databaseConnection = db.connect_database("Airbnb")
                if self.databaseConnection is not None:
                    statusLabel["text"] = "Connected to Airbnb DB"
                    connectionButton["text"] = "Disconnect from Airbnb DB"
            else:
                db.disconnect(self.databaseConnection)
                self.databaseConnection = None

                if self.databaseConnection is None:
                    statusLabel["text"] = "Disconnected"
                    connectionButton["text"] = "Connect to Airbnb DB"
