from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from user import User
from card import Card

class UserCard(Base):
    __tablename__ = "User_Card"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey=User.id)
    card_id = Column(Integer, ForeignKey=Card.id)
