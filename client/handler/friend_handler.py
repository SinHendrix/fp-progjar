from messages.add_friend_message import AddFriendMessage
from messages.message import Message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class FriendHandler:
    @staticmethod
    def input_add_friend_handle(sock_cli):
        friend_username = input("Masukkan username yang ingin dijadikan teman : ")
        add_friend_message = AddFriendMessage(
            friend_username,
        )
        message_string = pickle.dumps(add_friend_message)
        message_header = MessageHeader.make_header(
            MessageType.AddFriend,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_list_friend_handle(sock_cli):
        list_friend_message = Message()
        message_string = pickle.dumps(list_friend_message)
        message_header = MessageHeader.make_header(
            MessageType.ListFriend,
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
        friend_message = pickle.loads(message)

        print(friend_message.message)
