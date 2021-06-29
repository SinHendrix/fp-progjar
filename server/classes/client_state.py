import enum

class ClientState(enum.Enum):
    Login = 0
    Menu = 1
    Playing = 2
    Waiting = 3
    Turn = 4
    WaitForTurn = 5
    Chat = 6
    Shop = 7
