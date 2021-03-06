import string
import random

class Room:
    def __init__(self, name, players = []):
        self.name = name
        self.players = players

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

    @staticmethod
    def search_for_opponent(client):
        username = None

        for room in client.rooms:
            if room.players[0] == client.username:
                username = room.players[1]
                break
            elif room.players[1] == client.username:
                username = room.players[0]
                break

        for person in client.clients:
            if person.username == username:
                return person

    @staticmethod
    def delete_room(client):
        selected_room = None

        for room in client.rooms:
            if room.players[0] == client.username or room.players[1] == client.username:
                selected_room = room
                break

        client.rooms.remove(selected_room)
