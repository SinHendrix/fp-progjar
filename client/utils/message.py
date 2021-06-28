import settings

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
