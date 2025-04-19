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
