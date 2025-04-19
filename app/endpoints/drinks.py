from time import sleep

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud import create_drink, get_all_drinks, get_drink_by_id, update_drink, increment_amount_sold, delete_drink
from app.schemas import DrinkCreate, DrinkResponse
from app.database import get_db

router = APIRouter()


# Track whether a stock crash is currently active
stock_crash_active = False
temporary_prices = {}


@router.post("/drinks/stock-crash")
def stock_crash(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Stock crash: Temporarily set all drink prices to 2€ for 30 seconds.
    """
    global stock_crash_active, temporary_prices

    # Check if a stock crash is already active
    if stock_crash_active:
        return {"message": "Stock crash is already active."}

    # Fetch all drinks from the database and store their original prices
    drinks = get_all_drinks(db)
    temporary_prices = {drink.id: drink.price for drink in drinks}

    # Set the stock crash as active
    stock_crash_active = True

    # Start the background task to reset prices after 30 seconds
    background_tasks.add_task(reset_prices, db)

    return {"message": "Stock crash initiated. All prices are temporarily set to 1.50€."}


def reset_prices(db: Session):
    """
    Resets drink prices to their original values after the stock crash (30 seconds).
    """
    global stock_crash_active, temporary_prices

    # Wait for 30 seconds
    sleep(60)

    # Reset state
    stock_crash_active = False
    temporary_prices = {}


@router.post("/drinks/create", response_model=DrinkResponse)
def create(drink: DrinkCreate, db: Session = Depends(get_db)):
    return create_drink(db, drink)

@router.patch("/drinks/scale-amount/{drink_id}", response_model=DrinkResponse)
def scale_amount(drink_id: int, db: Session = Depends(get_db)):
    updated_drink = increment_amount_sold(db, drink_id)
    if not updated_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return updated_drink


@router.get("/drinks/get_all", response_model=list[DrinkResponse])
def read_all(db: Session = Depends(get_db)):
    """
        Returns the list of all drinks. If a stock crash is active, override all drink prices to 2€.
        """
    global temporary_prices

    # Fetch drinks from the database
    drinks = get_all_drinks(db)

    # If a stock crash is active, override the drink prices
    if temporary_prices:
        for drink in drinks:
            drink.price = 1.00  # Temporarily override price to €1.5 if stock crash is active

    return drinks

@router.get("/drinks/crash-status", response_model=dict)
def get_crash_status():
    """
    Returns whether or not a stock crash is currently active.
    """
    global stock_crash_active

    return {"crash_active": stock_crash_active}


@router.get("/drinks/single/{drink_id}", response_model=DrinkResponse)
def read_one(drink_id: int, db: Session = Depends(get_db)):
    db_drink = get_drink_by_id(db, drink_id)
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return db_drink


@router.put("/drinks/modify/{drink_id}", response_model=DrinkResponse)
def update(drink_id: int, updated_data: dict, db: Session = Depends(get_db)):
    updated_drink = update_drink(db, drink_id, updated_data)
    if not updated_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return updated_drink


@router.delete("/drinks/delete/{drink_id}", response_model=dict)
def delete(drink_id: int, db: Session = Depends(get_db)):
    deleted_drink = delete_drink(db, drink_id)
    if not deleted_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return {"message": "Drink deleted successfully"}