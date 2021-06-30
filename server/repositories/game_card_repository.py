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
    def print_cards(cards):
        counter = 1
        message = ""
        if len(cards) < 1:
            message = "Empty"
        else :
            for card in cards:
                message += "{}. {}\nAttack : {}\nDefence : {}\n".format(counter, card.name, card.attack, card.defence)
                counter += 1

        return message

    @staticmethod
    def handle_check_card_in_hand(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])
        message = receive_message(client.client, message_size)
        card_message = pickle.loads(message)
        message = GameCardRepository.print_cards(client.cards_in_hand)

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
        message = GameCardRepository.print_cards(client.cards_in_field)

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
        person = Room.search_for_opponent(client)
        message = GameCardRepository.print_cards(person.cards_in_field)

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
