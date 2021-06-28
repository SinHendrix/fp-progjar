import re
import settings

class MessageHeader:
    message_type = 0
    destination = 1
    message_size = 2
    sender = 3
    file_name = 4

    @staticmethod
    def make_header(
        message_type,
        destination,
        message_size,
        sender,
        file_name = ""
    ):
        return "|".join([message_type, destination, message_size, sender, file_name])

    @staticmethod
    def get_message_header(client):
        message_header = ""

        while len(re.findall('\n', message_header)) < 4:
            data = client.recv(1).decode(settings.ENCODING)

            if len(data) == 0:
                return ""
            message_header += data

        return message_header.split("|")
