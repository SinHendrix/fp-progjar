class JoinRoomMessage:
    def __init__(self, name, message = "", is_turn = False, success = False):
        self.name = name
        self.message = message
        self.success = success
        self.is_turn = is_turn
