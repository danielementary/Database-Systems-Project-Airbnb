from tkinter import *

class Interface(Frame):
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window, width=720, height=480, **kwargs)
        self.pack(fill=BOTH)

window = Tk()
window.title("DBS-Project")

interface = Interface(window)
interface.mainloop()
interface.destroy()
