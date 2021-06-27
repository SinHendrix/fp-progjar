import enum

class ClientState(enum.Enum):
    Menu = 1
    Chat = 2
    Waiting = 3
    Turn = 4
    WaitForTurn = 5
