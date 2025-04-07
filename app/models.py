from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount_sold = Column(Integer, default=0)
