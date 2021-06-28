from messages.register_message import RegisterMessage
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
from utils.menu import Menu
import pickle
import settings

class RegisterHandler:
    @staticmethod
    def input_handle(sock_cli):
        username = input("Masukkan username yang diinginkan : ")
        password = input("Masukkan password yang diinginkan : ")
        register_message = RegisterMessage(
            username,
            password
        )
        message_string = pickle.dumps(register_message)
        message_header = MessageHeader.make_header(
            MessageType.Register,
            'server',
            len(message_string),
            username
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def receive_message_handle(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        register_message = pickle.loads(message)

        print(register_message.message)

        if register_message.success:
            settings.CLIENT_STATE = ClientState.Menu
            settings.USERNAME = register_message.username
