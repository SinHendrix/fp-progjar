from messages.login_message import LoginMessage
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class LoginHandler:
    @staticmethod
    def input_handle(sock_cli):
        username = input("Masukkan username yang diinginkan : ")
        password = input("Masukkan password yang diinginkan : ")
        login_message = LoginMessage(
            username,
            password
        )
        message_string = pickle.dumps(login_message)
        message_header = MessageHeader.make_header(
            MessageType.Login,
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
        login_message = pickle.loads(message)

        print(login_message.message)

        if login_message.success:
            settings.CLIENT_STATE = ClientState.Menu
