from messages.message import Message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message, receive_file
from utils.file import File
import pickle
import settings
import os

class ChatHandler:
    @staticmethod
    def input_chat(sock_cli):
        settings.CLIENT_STATE = ClientState.Chat

    @staticmethod
    def input_text_message(sock_cli, in_waiting_room=False):
        destination = input("Insert destination of your message (bcast for broadcast to your friends) : ")
        message = input("Insert your message : ")
        text_message = Message()
        text_message.message = message
        message_string = pickle.dumps(text_message)
        message_header = MessageHeader.make_header(
            MessageType.Message,
            destination,
            len(message_string),
            settings.USERNAME
        )

        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

        if in_waiting_room:
            settings.CLIENT_STATE = ClientState.WaitingInRoom
        else :
            settings.CLIENT_STATE = ClientState.Menu

    @staticmethod
    def input_file_message(sock_cli, in_waiting_room=False):
        destination = input("Insert destination of your message (bcast for broadcast to your friends) : ")
        file_name = input("Insert picture name : ")
        file_route = settings.FILE_SENDED_ROUTE + file_name

        if not File.file_exists(file_name):
            print("File not exist")
            settings.CLIENT_STATE = ClientState.Menu
            return

        file_handler = open(file_route,'rb')
        data = file_handler.read()
        file_size = os.stat(file_route).st_size
        message_header = MessageHeader.make_header(
            MessageType.File,
            destination,
            file_size,
            settings.USERNAME,
            file_name=file_name
        )

        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, data)

        if in_waiting_room:
            settings.CLIENT_STATE = ClientState.WaitingInRoom
        else :
            settings.CLIENT_STATE = ClientState.Menu

    @staticmethod
    def receive_text_message_handle(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        message = pickle.loads(message)

        print("Receiving message from {} : ".format(message_header[MessageHeader.sender]), end='', flush=True)
        print(message.message, flush=True)

    @staticmethod
    def receive_file_message_handle(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]

        print("Receive picture {} from {}".format(message_header[MessageHeader.file_name], message_header[MessageHeader.sender]), flush=True)

        message = receive_file(sock_cli, message_header)
