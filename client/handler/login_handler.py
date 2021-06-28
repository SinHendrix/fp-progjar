from messages.login_message import LoginMessage
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from utils.message import send_message
import pickle

class LoginHandler:
    @staticmethod
    def input_handle(sock_cli):
        username = input("Masukkan username yang diinginkan : ")
        password = input("Masukkan password yang diinginkan : ")
        login_message = LoginMessage(
            username,
            password
        )
        message_string = pickle.dumps(register_message)
        message_header = MessageHeader.make_header(
            MessageType.Login,
            'server',
            len(message_string),
            username
        )
        send_message(sock_cli, bytes(message_header))
        send_message(sock_cli, message_string)
