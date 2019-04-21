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

        self.databaseSettingsFrame = ttk.Frame(self)
        self.databaseSettingsFrame.pack(fill=X)

        Label(self.databaseSettingsFrame, text="Status").pack(side=LEFT, padx=5, pady=5)

        self.statusLabel = Label(self.databaseSettingsFrame, text="Not Connected")
        self.statusLabel.pack(side=LEFT, padx=5, pady=5)

        self.connectionButton = Button(self.databaseSettingsFrame, text="Try again", command=lambda : self.connectDatabase())

        self.tabControl = ttk.Notebook(self)

        self.searchFrame        = ttk.Frame(self.tabControl)
        self.queriesFrame       = ttk.Frame(self.tabControl)
        self.modificationsFrame = ttk.Frame(self.tabControl)

        self.tabControl.add(self.searchFrame,        text="Search")
        self.tabControl.add(self.queriesFrame,       text="Predefined Queries")
        self.tabControl.add(self.modificationsFrame, text="Insert/Delete")

        self.tabControl.pack(fill=BOTH, expand=1)

        #search tab
        #search label
        Label(self.searchFrame, text="Search Box").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        #search search box
        self.searchBox = Entry(self.searchFrame)
        self.searchBox.grid(row=0, column=1, padx=5, pady=5)
        #search button
        self.searchButton = Button(self.searchFrame, text="Search", state=DISABLED)
        self.searchButton.grid(row=0, column=2, padx=5, pady=5)

        #queries tab
        Label(self.queriesFrame, text="This will be implemented later on.").pack()

        #modifications tab
        Label(self.modificationsFrame, text="This will be implemented later on.").pack()
        self.connectDatabase()

    def connectDatabase(self):
        if self.databaseConnection is None:
            self.databaseConnection = db.connect_database("Airbnb")

            if self.databaseConnection is not None:
                self.statusLabel["text"] = "Connected to Airbnb DB"
                self.connectionButton.pack_forget()
            else:
                self.statusLabel["text"] = "Please check that the MySQL server is running and configured"
                self.connectionButton.pack(side=LEFT, expand=1, anchor=E, padx=5, pady=5)
