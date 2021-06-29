from classes.client_state import ClientState
import settings

class Help:
    menu = {
        ClientState.Login : "1. Login\n2. Register",
        ClientState.Menu : "1. Chat\n2. Add a Friend\n3. List Friend\n4. Join a Room\n5. Make a Room\n6. Random Room\n7. Shop\n8. My Deck",
        ClientState.Chat : "1. Send Message\n2. Send Picture",
        ClientState.Shop : "1. Check Shop\n2. Buy\n3. Check Point\n4. Back",
    }

    general = "0. Help\n99. Exit"

    @staticmethod
    def get_menu():
        print(Help.menu[settings.CLIENT_STATE])

        if not ClientState.check_if_playing():
            print(Help.general)
