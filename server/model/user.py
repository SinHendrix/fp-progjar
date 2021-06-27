from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    points = Column(Integer)
    address = Column(String)
    port = Column(Integer)
