from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Drink
from app.schemas import DrinkCreate

# Dictionary to store runtime-tracked `last_updated` timestamps for drinks
# Key: drink_id, Value: datetime of last sale
last_updated_times = {}


# Create a new drink
def create_drink(db: Session, drink: DrinkCreate):
    db_drink = Drink(**drink.model_dump())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink


# Retrieve all drinks
def get_all_drinks(db: Session):
    PRICE_DECREMENT_AMOUNT = 0.10  # Price decreases by $0.10
    DECREASE_THRESHOLD = 1 * 60  # 2 minutes (threshold in seconds)

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

            # Cap the price to a minimum of $0.01
            drink.price = max(drink.price, 1.99)

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
def increment_amount_sold(db: Session, drink_id: int):
    db_drink = get_drink_by_id(db, drink_id)
    if not db_drink:
        return None

    # Save the current price in `old_price` before any adjustments
    db_drink.old_price = db_drink.price

    # Increment the `amount_sold` counter
    db_drink.amount_sold += 1

    # Pricing logic
    PRICE_INCREMENT_AMOUNT = 0.25
    DECREASE_THRESHOLD = 1 * 60  # 2 minutes (threshold in seconds)

    # Get the current time
    current_time = datetime.now()

    # Retrieve the last updated time from the runtime dictionary (default to a very old time)
    last_update = last_updated_times.get(drink_id, datetime.now() - timedelta(seconds=DECREASE_THRESHOLD + 1))
    time_since_last_update = (current_time - last_update).total_seconds()

    if db_drink.amount_sold % 5 == 0:
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
