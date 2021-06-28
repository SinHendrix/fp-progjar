import threading
import settings
from classes.message_type import MessageType
from classes.message_header import MessageHeader

class MessageReceiver(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            message_header = MessageHeader.get_message_header(self.client)

            if len(message_header) == 0:
                break

            if message_type == MessageType.Login:
                pass
            elif message_type == MessageType.Register:
                pass
            elif message_type == MessageType.AddFriend:
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
            elif message_type == MessageType.GetRoom:
                pass
            elif message_type == MessageType.Attack:
                pass
            else :
                continue
