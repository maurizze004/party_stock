from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    old_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    min_price = Column(Float, nullable=False)
    amount_sold = Column(Integer)
    revenue = Column(Float)
