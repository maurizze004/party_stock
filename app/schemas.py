from pydantic import BaseModel


class DrinkBase(BaseModel):
    name: str
    old_price: float
    price: float
    min_price: float
    amount_sold: int = 0  # Default value
    revenue: float = 0.0


class DrinkCreate(DrinkBase):
    pass  # For creating a new drink, all fields are inherited


class DrinkResponse(DrinkBase):
    id: int  # ID is included in the response

    class Config:
        orm_mode = True  # Enables ORM compatibility
