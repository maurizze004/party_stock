import multiprocessing
import threading
import webbrowser

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.endpoints import drinks
from app.database import engine, Base

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root URL / to the admin frontend
@app.get("/admin")
def redirect_to_admin():
    return RedirectResponse(url="/static/admin/index.html")
@app.get("/customer")
def redirect_to_admin():
    return RedirectResponse(url="/static/customer/index.html")
@app.get("/accounting")
def redirect_to_admin():
    return RedirectResponse(url="/static/accounting/index.html")
@app.get("/")
def redirect_to_admin():
    return RedirectResponse(url="/static/index.html")

# Register drinks router
app.include_router(drinks.router)

if __name__ == "__main__":
    multiprocessing.freeze_support()


    # Define a function to open the browser
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8000")  # Open the specified URL in a new browser tab


    # Start a background thread to open the browser (non-blocking)
    threading.Timer(1, open_browser).start()

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False, workers=1)