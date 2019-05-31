from tkinter import *
from tkinter import ttk

class Results(Toplevel):
    def __init__(self, master, queryResults, sql, values, **options):
        Toplevel.__init__(self, master, **options)
        self.title("DBS-Project Group32 Results")
        self.geometry("1400x800")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.closeResults)

        self.master.searchButton         ["state"] = DISABLED
        self.master.executeButton        ["state"] = DISABLED
        self.master.insertButton         ["state"] = DISABLED
        self.master.connectDatabaseButton["state"] = DISABLED
        self.master.deleteDatabaseButton ["state"] = DISABLED

        Label(self, text="Please close this windows before next operations.").pack(padx=10, pady=10)

        topFrame = Frame(self)
        topFrame.pack(expand=1, fill=BOTH, padx=10, pady=10)

        bottomFrame = Frame(self, bg="white")
        bottomFrame.pack(side=BOTTOM, expand=1, fill=BOTH, padx=10, pady=10)

        Label(topFrame, text="MySQL Statement : ", anchor=W).pack(side=LEFT, padx=10, pady=10, fill=BOTH)

        splitted = sql.split("\n")

        scrollbarSql = Scrollbar(topFrame)
        scrollbarSql.pack(side=LEFT, padx=10, pady=10, fill=BOTH)

        listboxSql = Listbox(topFrame)
        listboxSql.pack(side=LEFT, expand=1, fill=BOTH)

        for s in splitted:
            listboxSql.insert(END, s)

        listboxSql.config(yscrollcommand=scrollbarSql.set)
        scrollbarSql.config(command=listboxSql.yview)

        if (values is not None):
            Label(topFrame, text="with values : ", anchor=W).pack(side=LEFT, padx=10, pady=10, fill=BOTH)
            Label(topFrame, text=values, anchor=W).pack(side=LEFT, padx=10, pady=10, fill=BOTH)
        if (queryResults is not None):
            resultLength = len(queryResults)
            if (resultLength > 0):
                resultsScrollbarY = Scrollbar(bottomFrame)
                resultsScrollbarY.pack(side=LEFT, fill=Y)

                resultsListbox = Listbox(bottomFrame, yscrollcommand=resultsScrollbarY.set)
                resultsListbox.pack(side=LEFT, expand=1, fill=BOTH)

                resultsScrollbarY.config(command=resultsListbox.yview)

                self.sizes = [len(str(e)) for e in queryResults[0]]
                for r in queryResults:
                    self.sizes = self.maxSizes(self.sizes, [len(str(e)) for e in r])

                for r in queryResults:
                    temp = ""
                    c    = 0
                    for e in r:
                        temp += "{0:>{1}}".format(e, self.sizes[c]+15)
                        c    += 1
                    resultsListbox.insert(END, temp)
                Label(self, text="Results ({})".format(resultLength)).pack(side=BOTTOM, fill=X, padx=10, pady=10)
            else:
                Label(self, text="There are no results for this query.".format()).pack(side=BOTTOM, fill=X, padx=10, pady=10)
        else:
            Label(self, text="This query cannot be executed.".format()).pack(side=BOTTOM, fill=X, padx=10, pady=10)

    def maxSizes(self, list1, list2):
        lists = zip(list1, list2)
        return [max(e[0], e[1]) for e in lists]

    def closeResults(self):
        self.master.searchButton         ["state"] = NORMAL
        self.master.executeButton        ["state"] = NORMAL
        self.master.insertButton         ["state"] = NORMAL
        self.master.connectDatabaseButton["state"] = NORMAL
        self.master.deleteDatabaseButton ["state"] = NORMAL
        self.destroy()
