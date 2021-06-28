from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    points = Column(Integer)
    address = Column(String)
    port = Column(Integer)

    def __init__(self, username, password, points, address, port):
        self.username = username
        self.password = password
        self.points = points
        self.address = address
        self.port = port
