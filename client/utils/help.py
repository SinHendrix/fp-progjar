from classes.client_state import ClientState
import settings

class Help:
    menu = {
        ClientState.Login : """
        1. Login
        2. Register
        """,
        ClientState.Menu : """
        1. Chat
        2. Add a Friend
        3. Join a Room
        4. Make a Room
        5. Random Room
        """,
        ClientState.Chat : """
        1. Send Message
        2. Send Picture
        """
    }

    general = """
    0. Help
    99. Exit
    """

    @staticmethod
    def get_menu():
        print(menu[settings.CLIENT_STATE])

        if not ClientState.check_if_playing():
            print(general)
