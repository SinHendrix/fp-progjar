import threading
import ..settings
from ..class.message_header import MessageHeader

class Client(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client

    def get_message_header():
        message_header = ""

        while len(re.findall('\n', message_header)) < 4:
            data = self.client.recv(1).decode(settings.ENCODING)

            if len(data) == 0:
                return ""
            message_header += data

        return message_header.split("|")

    def run(self):
        while True:
            message_header = get_message_header()

            if len(message_header) == 0:
                break

            message_type = message_header[MessageHeader.message_type]
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
