import enum
import settings

class ClientState(enum.Enum):
    Login = 0
    Menu = 1
    Playing = 2
    Waiting = 3
    Turn = 4
    WaitForTurn = 5
    Chat = 6

    @staticmethod
    def check_if_playing():
        if settings.CLIENT_STATE not in [ClientState.Playing, ClientState.Waiting, ClientState.Turn, ClientState.WaitForTurn]:
            return True
        else:
            return False
