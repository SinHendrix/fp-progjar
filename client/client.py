import settings
import socket
from classes.message_receiver import MessageReceiver
from classes.client_state import ClientState
from utils.screen import clear_screen
from utils.menu import Menu
from utils.help import Help
from handler.exit import client_exit
from handler.login_handler import LoginHandler
from handler.register_handler import RegisterHandler
from handler.friend_handler import FriendHandler
from handler.deck_handler import DeckHandler

sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect((settings.ADDRESS, settings.PORT))
message_receiver = None

if __name__ == "__main__":
    message_receiver = MessageReceiver(sock_cli)
    message_receiver.start()

    try:
        while True:
            command = None

            try:
                Menu.prompting()
                command = Menu.get_command()
                clear_screen()
            except Exception as e:
                print("Insert the correct command")
                continue

            if settings.CLIENT_STATE ==  ClientState.Login and not Menu.check_if_help_or_menu(command) :
                if command == Menu.Login:
                    LoginHandler.input_handle(sock_cli)
                elif command == Menu.Register:
                    RegisterHandler.input_handle(sock_cli)
            elif settings.CLIENT_STATE == ClientState.Menu and not Menu.check_if_help_or_menu(command) :
                if command == Menu.AddFriend:
                    FriendHandler.input_add_friend_handle(sock_cli)
                elif command == Menu.ListFriend:
                    FriendHandler.input_list_friend_handle(sock_cli)
                elif command == Menu.Chat:
                    pass
                elif command == Menu.JoinRoom:
                    pass
                elif command == Menu.MakeRoom:
                    pass
                elif command == Menu.JoinRoom:
                    pass
                elif command == Menu.RandomRoom:
                    pass
                elif command == Menu.Shop:
                    pass
                elif command == Menu.MyDeck:
                    DeckHandler.handle(sock_cli)
            elif settings.CLIENT_STATE == ClientState.Turn and not Menu.check_if_help_or_menu(command) :
                if message_type == MessageType.Attack:
                    pass
            elif command == Menu.Help :
                Help.get_menu()
            elif command == Menu.Exit and not ClientState.check_if_playing():
                client_exit(message_receiver)
                break
            else :
                continue
    except Exception as e:
        print(e)
        client_exit(message_receiver)
