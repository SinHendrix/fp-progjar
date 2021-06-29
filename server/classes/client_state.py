import enum

class ClientState(enum.Enum):
    Login = 0
    Menu = 1
    Playing = 2
    WaitingInRoom = 3
    WaitingInWaitingRoom = 4
    Turn = 5
    WaitForTurn = 6
    Chat = 7
    Shop = 8

    @staticmethod
    def check_if_playing(client):
        if client.state in [ClientState.Playing, ClientState.WaitingInRoom, ClientState.WaitingInWaitingRoom, ClientState.Turn, ClientState.WaitForTurn]:
            return True
        else:
            return False
