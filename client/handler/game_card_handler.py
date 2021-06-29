from messages.message import Message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class GameCardHandler:
    @staticmethod
    def input_check_card_in_hand(sock_cli):
        message = Message()
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.CheckCardInHand,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_check_card_in_own_field(sock_cli):
        message = Message()
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.CheckCardInOwnField,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_check_card_in_enemy_field(sock_cli):
        message = Message()
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.CheckCardInEnemyField,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def receive_message_handle(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        deck_message = pickle.loads(message)

        print(deck_message.message)
