from models.user import User
from models.user_card import UserCard
from models.base import session
from messages.join_room_message import JoinRoomMessage
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from classes.room import Room
import pickle
import settings
import copy

class RoomRepository:
    @staticmethod
    def make_room_handle(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        message = pickle.loads(message)

        room = Room(
            Room.random_room_name(client.rooms),
            players=[client.username]
        )

        client.state = ClientState.WaitingInRoom
        client.rooms.append(room)

        message.success = True
        message.message = "Your room code is : {}".format(room.name)
        message = pickle.dumps(message)
        new_message_header = MessageHeader.make_header(
            MessageType.MakeRoom,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def join_room_handle(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        join_room_message = receive_message(client.client, message_size)
        join_room_message = pickle.loads(join_room_message)

        room_found = False
        for room in client.rooms:
            if room.name == join_room_message.name:
                room_found = True
                person_message = copy.copy(join_room_message)
                person_message.message = "Found opponent ({})".format(client.username)
                person_message.success = True
                person_message.is_turn = True
                person_message = pickle.dumps(person_message)
                person_new_message_header = MessageHeader.make_header(
                    MessageType.JoinRoom,
                    client.username,
                    len(person_message),
                    'server'
                )

                for person in client.clients:
                    if person.username == room.players[0]:
                        send_message(person.client, bytes(person_new_message_header, settings.ENCODING))
                        send_message(person.client, person_message)

                        person.state = ClientState.Playing

                        room.players.append(client.username)
                        join_room_message.message = "Found opponent ({})".format(person.username)
                        break
                break

        if not room_found:
            join_room_message.success = False
            join_room_message.message = "Room not found"
            join_room_message = pickle.dumps(join_room_message)
            new_message_header = MessageHeader.make_header(
                MessageType.JoinRoom,
                client.username,
                len(join_room_message),
                'server'
            )

            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, join_room_message)
            return

        client.state = ClientState.WaitForTurn

        join_room_message.success = True
        join_room_message = pickle.dumps(join_room_message)
        new_message_header = MessageHeader.make_header(
            MessageType.JoinRoom,
            client.username,
            len(join_room_message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, join_room_message)
