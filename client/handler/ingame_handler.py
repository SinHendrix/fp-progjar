from messages.ingame_message import IngameMessage
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from utils.message import send_message, receive_message
import pickle
import settings

class IngameHandler:
    @staticmethod
    def input_draw_card(sock_cli):
        try:
            card_number = int(input("Masukkan nomor kartu yang ingin di-draw : "))
        except Exception as e:
            print("Masukkan angka dengan benar")
            return
        message = IngameMessage(card_number)
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.DrawCard,
            'server',
            len(message_string),
            settings.USERNAME
        )
        send_message(sock_cli, bytes(message_header, settings.ENCODING))
        send_message(sock_cli, message_string)

    @staticmethod
    def input_attack(sock_cli):
        try:
            card_number_1 = int(input("Masukkan nomor kartu yang akan menyerang : "))
            card_number_2 = int(input("Masukkan nomor kartu yang akan diserang : "))
            message = IngameMessage(card_number_1, card_number_2=card_number_2)
        except Exception as e:
            print("Masukkan angka dengan benar")
            return
        message_string = pickle.dumps(message)
        message_header = MessageHeader.make_header(
            MessageType.Attack,
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
        message = pickle.loads(message)

        print(message.message)

        if message.success:
            if message.finished :
                settings.CLIENT_STATE = ClientState.Menu
            elif settings.CLIENT_STATE == ClientState.WaitForTurn:
                settings.CLIENT_STATE = ClientState.Playing
            else :
                settings.CLIENT_STATE = ClientState.WaitForTurn
