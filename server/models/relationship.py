from models.base import Base, session
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

    @staticmethod
    def check_if_friend(username_1, username_2):
        user_1 = User.get_user_by_username(username_1)[0]
        user_2 = User.get_user_by_username(username_2)[0]

        relationships = session.query(Relationship).filter_by(
            user_id_1=user_1.id,
            user_id_2=user_2.id,
        ).all()

        if len(relationships) < 1:
            return False
        else :
            return True
