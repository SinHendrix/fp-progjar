import threading
import settings
import re
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from repositories.register_repository import RegisterRepository
from repositories.login_repository import LoginRepository
from repositories.friend_repository import FriendRepository
from repositories.deck_repository import DeckRepository
from repositories.shop_repository import ShopRepository
from repositories.room_repository import RoomRepository


class Client(threading.Thread):
    def __init__(self, client, address, clients, rooms, user_waiting):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.state = ClientState.Login
        self.username = ""
        self.clients = clients
        self.rooms = rooms
        self.user_waiting = user_waiting

    def change_state(new_state):
        self.state = new_state

    def run(self):
        while True:
            try:
                message_header = MessageHeader.get_message_header(self.client)

                if len(message_header) == 0:
                    break

                message_type = message_header[MessageHeader.message_type]

                if self.state ==  ClientState.Login and not MessageHeader.header_is_exit(message_header):
                    if message_type == MessageType.Login:
                        LoginRepository.handle(self, message_header)
                    elif message_type == MessageType.Register:
                        RegisterRepository.handle(self, message_header)
                elif self.state == ClientState.Menu and not MessageHeader.header_is_exit(message_header):
                    if message_type == MessageType.AddFriend:
                        FriendRepository.handle_add_friend(self, message_header)
                    elif message_type == MessageType.ListFriend:
                        FriendRepository.handle_list_friend(self, message_header)
                    elif message_type == MessageType.Message:
                        pass
                    elif message_type == MessageType.File:
                        pass
                    elif message_type == MessageType.MakeRoom:
                        RoomRepository.make_room_handle(self, message_header)
                    elif message_type == MessageType.JoinRoom:
                        RoomRepository.join_room_handle(self, message_header)
                    elif message_type == MessageType.Shop:
                        pass
                    elif message_type == MessageType.MyDeck:
                        DeckRepository.handle(self, message_header)
                    elif message_type == MessageType.CheckShop:
                        ShopRepository.handle_check_shop(self, message_header)
                    elif message_type == MessageType.CheckPoint:
                        ShopRepository.handle_check_point(self, message_header)
                    elif message_type == MessageType.Buy:
                        ShopRepository.handle_buy(self, message_header)
                elif self.state == ClientState.Turn and not MessageHeader.header_is_exit(message_header):
                    if message_type == MessageType.Attack:
                        pass
                elif MessageHeader.header_is_exit(message_header):
                    print("Client ", self.address, " Exited")
                    self.clients.remove(self)
                    break
            except Exception as e:
                print(e, flush=True)
