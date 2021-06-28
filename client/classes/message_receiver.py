import threading
import settings
import ctypes
from classes.message_type import MessageType
from classes.message_header import MessageHeader
from handler.register_handler import RegisterHandler
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

            if message_type == MessageType.Login:
                pass
            elif message_type == MessageType.Register:
                RegisterHandler.receive_message_handle(self.client, message_header)
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
