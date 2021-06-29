from models.user import User
from models.user_card import UserCard
from models.card import Card
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from sqlalchemy import func
from classes.room import Room
import pickle
import settings

class GameCardRepository:
    @staticmethod
    def handle_check_card_in_hand(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        card_message = pickle.loads(message)

        message = ""

        for card in client.cards_in_hand:
            message += "- {}\nAttack : {}\nDefence : {}".format(card.name, card.attack, card.defence)

        card_message.success = True
        card_message.message = message
        message = pickle.dumps(card_message)
        new_message_header = MessageHeader.make_header(
            MessageType.CheckCardInHand,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_check_card_in_own_field(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        card_message = pickle.loads(message)

        message = ""

        if len(client.cards_in_field) < 1:
            message = "The field is empty"
        else :
            for card in client.cards_in_field:
                message += "- {}\nAttack : {}\nDefence : {}".format(card.name, card.attack, card.defence)

        card_message.success = True
        card_message.message = message
        message = pickle.dumps(card_message)
        new_message_header = MessageHeader.make_header(
            MessageType.CheckCardInOwnField,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_check_card_in_enemy_field(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        card_message = pickle.loads(message)

        message = ""

        person = Room.search_for_opponent(client)

        if len(person.cards_in_field) < 1:
            message = "The field is empty"
        else :
            for card in person.cards_in_field:
                message += "- {}\nAttack : {}\nDefence : {}".format(card.name, card.attack, card.defence)

        card_message.success = True
        card_message.message = message
        message = pickle.dumps(card_message)
        new_message_header = MessageHeader.make_header(
            MessageType.CheckCardInEnemyField,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
