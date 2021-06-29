import string
import random

class Room:
    def __init__(self, name, players = []):
        self.name = name
        self.players = players
        self.turn_player_0 = True
        self.turn_player_0_counter = 0
        self.turn_player_1_counter = 0
        self.round = 1

    def change_turn():
        self.turn_player_0 = not self.turn_player_0

    def is_first_round():
        return self.round == 1

    def next_round():
        self.round += 1

    def is_room_full():
        return len(self.players) >= 2

    @staticmethod
    def random_room_name(rooms):
        room_name = None

        while True:
            name_not_used = True
            room_name = ''.join([random.choice(string.ascii_letters) for i in range(6)])

            for room in rooms:
                if room.name == room_name:
                    name_not_used = False
                    break

            if not name_not_used:
                continue
            else :
                break

        return room_name
