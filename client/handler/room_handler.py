from messages.message import Message
from messages.join_room_message import JoinRoomMessage
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class RoomHandler:
    @staticmethod
    def input_make_room_handle(sock_cli):
        message = JoinRoomMessage("")
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.MakeRoom,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_join_room_handle(sock_cli):
        room_name = input("Insert room code : ")
        join_room_message = JoinRoomMessage(room_name)
        message_string = pickle.dumps(join_room_message)
        message_header = MessageHeader.make_header(
            MessageType.JoinRoom,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_random_room_handle(sock_cli):
        message = JoinRoomMessage("")
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.RandomRoom,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def receive_message_handle_make_room(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        message = pickle.loads(message)

        print(message.message, flush=True)

        if message.success:
            settings.ROOM_CODE = message.name
            settings.CLIENT_STATE = ClientState.WaitingInRoom

    @staticmethod
    def receive_message_handle_join_room(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        join_room_message = receive_message(sock_cli, message_size)
        join_room_message = pickle.loads(join_room_message)

        print(join_room_message.message, flush=True)

        if join_room_message.success:
            if join_room_message.is_turn:
                settings.CLIENT_STATE = ClientState.Playing
            else :
                settings.CLIENT_STATE = ClientState.WaitForTurn

    @staticmethod
    def receive_message_handle_random_room(sock_cli, message_header):
        message_size = message_header[MessageHeader.message_size]
        message = receive_message(sock_cli, message_size)
        message = pickle.loads(message)

        print(message.message, flush=True)

        if message.success:
            settings.CLIENT_STATE = ClientState.WaitingInWaitingRoom