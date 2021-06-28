class LoginMessage:
    username = None
    password = None

    def __init__(self, username, password, success = False):
        self.username = username
        self.password = password
        self.success = success
