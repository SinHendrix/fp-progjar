from models.base import Base
from models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey

class Relationship(Base):
    __tablename__ = "Relationships"
    id = Column(Integer, primary_key=True)
    user_id_1 = Column(Integer)
    user_id_2 = Column(Integer)

    def __init__(self, user_id_1, user_id_2):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
