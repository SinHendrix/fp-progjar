import settings
from classes.message_header import MessageHeader

def send_message(sock_cli, message):
    sock_cli.send(message)

def receive_message(sock_cli, message_size):
    received_size = 0
    message = b''

    while received_size < int(message_size):
        data = sock_cli.recv(settings.BATCH_SIZE)
        received_size += len(data)
        message += data

    return message

def receive_file(sock_cli, message_header):
    received_size = 0
    file_name = message_header[MessageHeader.file_name]
    file_size = int(message_header[MessageHeader.message_size])

    with open(settings.FILE_RECEIVED_ROUTE + file_name, "wb") as file:
        while received_size < file_size:
            data = sock_cli.recv(settings.BATCH_SIZE)
            received_size += len(data)

            file.write(data)
