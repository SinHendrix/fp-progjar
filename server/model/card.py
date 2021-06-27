from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Card(Base):
    __tablename__ = "Cards"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    attack = Column(Integer)
    defence = Column(Integer)
    price = Column(Integer)
