import threading
import traceback
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
from repositories.game_card_repository import GameCardRepository
from repositories.ingame_repository import IngameRepository
from repositories.chat_repository import ChatRepository


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
        self.cards_in_hand = []
        self.cards_in_field = []

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
                        ChatRepository.handle_text_message(self, message_header)
                    elif message_type == MessageType.File:
                        ChatRepository.handle_file_message(self, message_header)
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
                elif self.state == ClientState.WaitingInRoom and not MessageHeader.header_is_exit(message_header):
                    if message_type == MessageType.Message:
                        ChatRepository.handle_text_message(self, message_header)
                elif ClientState.check_if_playing(self) and not MessageHeader.header_is_exit(message_header):
                    if message_type == MessageType.CheckCardInHand:
                        GameCardRepository.handle_check_card_in_hand(self, message_header)
                    elif message_type == MessageType.CheckCardInOwnField:
                        GameCardRepository.handle_check_card_in_own_field(self, message_header)
                    elif message_type == MessageType.CheckCardInEnemyField:
                        GameCardRepository.handle_check_card_in_enemy_field(self, message_header)
                    elif message_type == MessageType.DrawCard:
                        IngameRepository.handle_draw_card(self, message_header)
                    elif message_type == MessageType.Attack:
                        IngameRepository.handle_attack(self, message_header)
                elif MessageHeader.header_is_exit(message_header):
                    print("Client ", self.address, " Exited")
                    self.clients.remove(self)
                    break
            except Exception as e:
                print(e, flush=True)
                print(traceback.format_exc(), flush=True)
