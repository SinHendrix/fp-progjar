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
