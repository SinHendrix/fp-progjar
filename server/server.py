from classes.client import Client
from models import base
import socket
import threading
import settings


sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind((settings.ADDRESS, settings.PORT))
sock_server.listen(5)

clients = []

if __name__ == "__main__":
    print("Server running with address {}".format(settings.ADDRESS + ":" + str(settings.PORT)))

    while True:
        client_socket, client_address = sock_server.accept()
        client = Client(client_socket, client_address, clients)
        client.start()
        clients.append(client)

        print("client with address {} connected".format(client_address))

    for c in clients:
        c.join()

    sock_server.close()
