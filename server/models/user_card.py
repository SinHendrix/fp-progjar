from models.base import Base, session
from models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey, func

class UserCard(Base):
    __tablename__ = "User_Card"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    card_id = Column(Integer)

    def __init__(self, user_id, card_id):
        self.user_id = user_id
        self.card_id = card_id

    @staticmethod
    def get_user_cards_by_username(username):
        user = User.get_user_by_username(username)[0]
        return session.query(UserCard.card_id, func.count(UserCard.card_id)).group_by(UserCard.card_id).filter_by(user_id=user.id).all()
