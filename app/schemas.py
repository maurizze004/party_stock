from pydantic import BaseModel


class DrinkBase(BaseModel):
    name: str
    price: float
    amount_sold: int = 0  # Default value


class DrinkCreate(DrinkBase):
    pass  # For creating a new drink, all fields are inherited


class DrinkResponse(DrinkBase):
    id: int  # ID is included in the response

    class Config:
        orm_mode = True  # Enables ORM compatibility
