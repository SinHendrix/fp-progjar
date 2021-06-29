from models.user import User
from models.user_card import UserCard
from models.card import Card
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from sqlalchemy import func
import pickle
import settings

class DeckRepository:
    @staticmethod
    def handle(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        deck_message = pickle.loads(message)

        user = User.get_user_by_username(client.username)[0]
        user_cards = session.query(UserCard.card_id, func.count(UserCard.card_id)).group_by(UserCard.card_id).filter_by(user_id=user.id).all()

        message = ""

        for user_card in user_cards:
            card = session.query(Card).filter_by(id=user_card[0]).all()[0]
            message += "- {}\nAttack : {}\nDefence : {}\nStock : {}\n".format(card.name, card.attack, card.defence, user_card[1])

        deck_message.success = True
        deck_message.message = message
        message = pickle.dumps(deck_message)
        new_message_header = MessageHeader.make_header(
            MessageType.MyDeck,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
