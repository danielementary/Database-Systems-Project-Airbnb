from tkinter import *
from tkinter import ttk

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.title("DBS-Project Group32")
        self.geometry("720x480")
        self.resizable(width=False, height=False)

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
