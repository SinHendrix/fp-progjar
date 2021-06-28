from classes.client_state import ClientState
import settings

class Help:
    menu = {
        ClientState.Login : "1. Login\n2. Register",
        ClientState.Menu : "1. Chat\n2. Add a Friend\n3. Join a Room\n4. Make a Room\n5. Random Room",
        ClientState.Chat : "1. Send Message\n2. Send Picture"
    }

    general = "0. Help\n99. Exit"

    @staticmethod
    def get_menu():
        print(Help.menu[settings.CLIENT_STATE])

        if not ClientState.check_if_playing():
            print(Help.general)
