from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class UserCard(Base):
    __tablename__ = "User_Card"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    card_id = Column(Integer)

    def __init__(self, user_id, card_id):
        self.user_id = user_id
        self.card_id = card_id
