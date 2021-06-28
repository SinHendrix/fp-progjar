import settings
import socket
from classes.message_receiver import MessageReceiver
from classes.client_state import ClientState
from utils.screen import clear_screen
from utils.menu import Menu
from utils.help import Help
from handler.exit import client_exit

sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect((settings.ADDRESS, settings.PORT))
message_receiver = None

if __name__ == "__main__":
    message_receiver = MessageReceiver(sock_cli)
    message_receiver.start()

    while True:
        command = None

        try:
            Menu.prompting()
            command = Menu.get_command()
            clear_screen()
        except Exception as e:
            print("Insert the correct command")
            continue

        if settings.CLIENT_STATE ==  ClientState.Login:
            if command == Menu.Login:
                pass
            elif command == Menu.Register:
                pass
        elif settings.CLIENT_STATE == ClientState.Menu :
            if command == Menu.AddFriend:
                pass
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
        elif settings.CLIENT_STATE == ClientState.Turn:
            if message_type == MessageType.Attack:
                pass
        elif command == Menu.Help :
            Help.get_menu()
        elif command == Menu.Exit and not ClientState.check_if_playing():
            client_exit(message_receiver.client)
        else :
            continue
