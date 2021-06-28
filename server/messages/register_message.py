class RegisterMessage:
    username = None
    password = None

    def __init__(self, username, password, message = "", success = False):
        self.username = username
        self.password = password
        self.message = message
        self.success = success
