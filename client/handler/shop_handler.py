from messages.message import Message
from messages.buy_card_message import BuyCardMessage
from messages.message import Message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class ShopHandler:
    @staticmethod
    def input_check_shop_handle(sock_cli):
        message = Message()
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.CheckShop,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_check_point_handle(sock_cli):
        message = Message()
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.CheckPoint,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_buy_handle(sock_cli):
        card = int(input("Masukkan nomor kartu yang diinginkan : "))
        buy_card_message = BuyCardMessage(card)
        message_string = pickle.dumps(buy_card_message)
        message_header = MessageHeader.make_header(
            MessageType.Buy,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_back_handle(sock_cli):
        settings.CLIENT_STATE = ClientState.Menu

    @staticmethod
    def input_shop_handle(sock_cli):
        settings.CLIENT_STATE = ClientState.Shop

    @staticmethod
    def receive_message_handle(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        friend_message = pickle.loads(message)

        print(friend_message.message)
