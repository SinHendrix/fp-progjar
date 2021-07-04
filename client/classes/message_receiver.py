import threading
import settings
import ctypes
from classes.message_type import MessageType
from classes.message_header import MessageHeader
from handler.register_handler import RegisterHandler
from handler.friend_handler import FriendHandler
from handler.login_handler import LoginHandler
from handler.deck_handler import DeckHandler
from handler.shop_handler import ShopHandler
from handler.room_handler import RoomHandler
from handler.game_card_handler import GameCardHandler
from handler.ingame_handler import IngameHandler
from handler.chat_handler import ChatHandler
from utils.screen import clear_screen
from utils.menu import Menu

class MessageReceiver(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            message_header = MessageHeader.get_message_header(self.client)

            if len(message_header) == 0:
                break

            message_type = message_header[MessageHeader.message_type]

            print('\n', end='', flush=True)

            if message_type == MessageType.Login:
                LoginHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.Register:
                RegisterHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.AddFriend:
                FriendHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.ListFriend:
                FriendHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.Message:
                ChatHandler.receive_text_message_handle(self.client, message_header)
            elif message_type == MessageType.File:
                ChatHandler.receive_file_message_handle(self.client, message_header)
            elif message_type == MessageType.MakeRoom:
                RoomHandler.receive_message_handle_make_room(self.client, message_header)
            elif message_type == MessageType.JoinRoom:
                RoomHandler.receive_message_handle_join_room(self.client, message_header)
            elif message_type == MessageType.Attack:
                pass
            elif message_type == MessageType.Shop:
                ShopHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.MyDeck:
                DeckHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.CheckCardInHand:
                GameCardHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.CheckCardInOwnField:
                GameCardHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.CheckCardInEnemyField:
                GameCardHandler.receive_message_handle(self.client, message_header)
            elif message_type == MessageType.Ingame:
                IngameHandler.receive_message_handle(self.client, message_header)
            else :
                continue

            Menu.prompting()

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Client Stopped")
