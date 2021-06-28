import threading
import settings
import re
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState


class Client(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.state = ClientState.Login
        self.username = ""

    def change_state(new_state):
        self.state = new_state

    def run(self):
        while True:
            message_header = MessageHeader.get_message_header(self.client)

            if len(message_header) == 0:
                break

            message_type = message_header[MessageHeader.message_type]

            if self.state ==  ClientState.Login:
                if message_type == MessageType.Login:
                    pass
                elif message_type == MessageType.Register:
                    pass
                else :
                    continue
            elif self.state == ClientState.Menu :
                if message_type == MessageType.AddFriend:
                    pass
                elif message_type == MessageType.Message:
                    pass
                elif message_type == MessageType.File:
                    pass
                elif message_type == MessageType.MakeRoom:
                    pass
                elif message_type == MessageType.JoinRoom:
                    pass
                elif message_type == MessageType.RandomRoom:
                    pass
                else :
                    continue
            elif self.state == ClientState.Turn:
                if message_type == MessageType.Attack:
                    pass
                else :
                    continue
            else :
                continue
