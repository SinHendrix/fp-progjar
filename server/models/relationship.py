from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from user import User

class Relationship(Base):
    __tablename__ = "Relationships"
    id = Column(Integer, primary_key=True)
    user_id_1 = Column(Integer, ForeignKey=User.id)
    user_id_2 = Column(Integer, ForeignKey=User.id)
