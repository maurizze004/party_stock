from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_drink, get_all_drinks, get_drink_by_id, update_drink, delete_drink
from app.schemas import DrinkCreate, DrinkResponse
from app.database import get_db

router = APIRouter()


@router.post("/drinks/create", response_model=DrinkResponse)
def create(drink: DrinkCreate, db: Session = Depends(get_db)):
    return create_drink(db, drink)


@router.get("/drinks/get_all", response_model=list[DrinkResponse])
def read_all(db: Session = Depends(get_db)):
    return get_all_drinks(db)


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
