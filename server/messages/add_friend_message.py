class AddFriendMessage:
    username = None
    password = None

    def __init__(self, friend_username, message = "", success = False):
        self.friend_username = friend_username
        self.message = message
        self.success = success
