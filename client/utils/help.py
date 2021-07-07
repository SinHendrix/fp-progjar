from classes.client_state import ClientState
import settings

class Help:
    menu = {
        ClientState.Login : "1. Login\n2. Register",
        ClientState.Menu : "1. Chat\n2. Add a Friend\n3. List Friend\n4. Join a Room\n5. Make a Room\n6. Shop\n7. My Deck\n8. Random Room",
        ClientState.Chat : "1. Send Message\n2. Send Picture",
        ClientState.Shop : "1. Check Shop\n2. Buy\n3. Check Point\n4. Back",
        ClientState.WaitingInRoom : "Waiting in room...",
        ClientState.WaitingInWaitingRoom : "In waiting room...",
        ClientState.Playing : "1. Check Card in Hand\n2. Check Card in Own Field\n3. Check Card in Enemy Field\n4. Draw Card\n5. Attack",
        ClientState.WaitForTurn : "1. Check Card in Hand\n2. Check Card in Own Field\n3. Check Card in Enemy Field",
        ClientState.Chat : "1. Send Text Message\n2. Send Picture",
    }

    general = "0. Help\n99. Exit"

    @staticmethod
    def get_menu():
        print(Help.menu[settings.CLIENT_STATE])

        if not ClientState.check_if_playing():
            print(Help.general)
        
        if settings.CLIENT_STATE == ClientState.WaitingInRoom:
            print("Room Code : {}\n1. Send Message to Friends".format(settings.ROOM_CODE))
