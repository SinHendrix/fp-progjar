import threading
import ..settings

class MessageReceiver(threading.Thread):
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
            get_message_header()
