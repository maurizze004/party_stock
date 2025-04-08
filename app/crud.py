from sqlalchemy.orm import Session
from app.models import Drink
from app.schemas import DrinkCreate


# Create a new drink
def create_drink(db: Session, drink: DrinkCreate):
    db_drink = Drink(**drink.dict())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink


# Retrieve all drinks
def get_all_drinks(db: Session):
    return db.query(Drink).all()


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
    if db_drink:
        db_drink.amount_sold += 1  # Increment the amount_sold field
        db.commit()
        db.refresh(db_drink)  # Refresh the instance
        return db_drink
    return None  # If drink doesn't exist


# Delete a drink
def delete_drink(db: Session, drink_id: int):
    db_drink = get_drink_by_id(db, drink_id)
    if db_drink:
        db.delete(db_drink)
        db.commit()
    return db_drink
