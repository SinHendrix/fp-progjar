from models.base import Base
from models.base import session
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

    @staticmethod
    def get_user_by_id(id):
        return session.query(User).filter_by(id=id).all()

    @staticmethod
    def get_user_by_username(username):
        return session.query(User).filter_by(username=username).all()
