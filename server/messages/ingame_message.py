class IngameMessage:
    def __init__(self, card_number_1, card_number_2 = None, message = "", success = False, finished = False):
        self.card_number_1 = card_number_1
        self.card_number_2 = card_number_2
        self.message = message
        self.success = success
        self.finished = finished
