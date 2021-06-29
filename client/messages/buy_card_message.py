class BuyCardMessage:
    def __init__(self, card, message = "", success = False):
        self.card = card
        self.message = message
        self.success = success
