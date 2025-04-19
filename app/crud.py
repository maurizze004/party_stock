from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Drink
from app.schemas import DrinkCreate

# Dictionary to store runtime-tracked `last_updated` timestamps for drinks
# Key: drink_id, Value: datetime of last sale
last_updated_times = {}
def get_stock_crash_active():
    from app.endpoints.drinks import stock_crash_active
    return stock_crash_active

# Create a new drink
def create_drink(db: Session, drink: DrinkCreate):
    db_drink = Drink(**drink.model_dump())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink


# Retrieve all drinks
# Here modifiable:  The decrease rate and threshold
def get_all_drinks(db: Session):
    PRICE_DECREMENT_AMOUNT = 0.10  # Price decreases by €0.10
    DECREASE_THRESHOLD = 2 * 60  # 2 minutes (threshold in seconds)

    # Get the current time
    current_time = datetime.now()

    # Retrieve all drinks from the database
    drinks = db.query(Drink).all()

    # Iterate over each drink to handle price decrement logic
    for drink in drinks:
        # Make sure the last_updated time is tracked
        last_update = last_updated_times.get(drink.id, datetime.now() - timedelta(seconds=DECREASE_THRESHOLD + 1))

        # Calculate the time difference since the last sale or update
        time_since_last_update = (current_time - last_update).total_seconds()

        # Price Decrement Logic: No sale for 2+ minutes
        if time_since_last_update > DECREASE_THRESHOLD:
            # Save the current price in `old_price`
            drink.old_price = drink.price

            # Decrease the price
            drink.price -= PRICE_DECREMENT_AMOUNT

            # Cap the price to a minimum of database min_price
            drink.price = max(drink.price, drink.min_price)

            # Update the runtime `last_updated` time
            last_updated_times[drink.id] = current_time

    # Commit changes to the database
    db.commit()

    # Return the updated list of drinks
    return drinks


# Retrieve a drink by its ID
def get_drink_by_id(db: Session, drink_id: int):
    return db.query(Drink).filter(Drink.id == drink_id).first()


# Update a drink
def update_drink(db: Session, drink_id: int, updated_data: dict):
    db_drink = get_drink_by_id(db, drink_id)
    if db_drink:
        for key, value in updated_data.items():
            setattr(db_drink, key, value)
        db.commit()
        db.refresh(db_drink)
    return db_drink


# Increment the amount_sold of a drink by 1
# Here modifiable:  Delete '#' in line 92 and rücke line 93 ein in for incrementing every X amount sold; default every 3rd
def increment_amount_sold(db: Session, drink_id: int):
    db_drink = get_drink_by_id(db, drink_id)
    if not db_drink:
        return None

    # Save the current price in `old_price` before any adjustments
    db_drink.old_price = db_drink.price

    # Increment the `amount_sold` counter
    db_drink.amount_sold += 1

    # add here price for accounting
    if get_stock_crash_active():
        db_drink.revenue += 1.00
    else:
        db_drink.revenue += db_drink.price

    # Pricing logic
    PRICE_INCREMENT_AMOUNT = 0.30

    # if db_drink.amount_sold % 3 == 0:
    db_drink.price += PRICE_INCREMENT_AMOUNT

    # Save changes to the database
    db.commit()
    db.refresh(db_drink)
    return db_drink


# Delete a drink
def delete_drink(db: Session, drink_id: int):
    db_drink = get_drink_by_id(db, drink_id)
    if db_drink:
        db.delete(db_drink)
        db.commit()
    return db_drink