from src.app import App
from src.database import disconnect

def disconnect_and_close(app):
    disconnect(app.databaseConnection)
    app.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", lambda: disconnect_and_close(app))
    app.mainloop()
