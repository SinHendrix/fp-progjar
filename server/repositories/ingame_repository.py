from models.user import User
from models.user_card import UserCard
from models.card import Card
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from messages.ingame_message import IngameMessage
from sqlalchemy import func
from classes.room import Room
import pickle
import settings

class IngameRepository:
    @staticmethod
    def send_opponent_message(client, message, finished = False):
        opponent = Room.search_for_opponent(client)

        ingame_message = IngameMessage(0)
        ingame_message.success = True
        ingame_message.message = message
        ingame_message.finished = finished
        ingame_message = pickle.dumps(ingame_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Ingame,
            opponent.username,
            len(message),
            'server'
        )

        send_message(opponent.client, bytes(new_message_header, settings.ENCODING))
        send_message(opponent.client, ingame_message)

    @staticmethod
    def filter_died_card(client, message):
        dead_card = []

        for card in client.cards_in_field:
            if card.defence <= 0:
                dead_card.append(card)
                message += "{}'s {} dead\n".format(client.username, card.name)

        for card in dead_card:
            client.cards_in_field.remove(card)

        return message

    @staticmethod
    def check_if_lose(client):
        return len(client.cards_in_hand) < 1 and len(client.cards_in_field) < 1

    @staticmethod
    def handle_draw_card(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])
        message = receive_message(client.client, message_size)
        message = pickle.loads(message)
        new_message_header = None

        if len(client.cards_in_hand) < 1 or message.card_number_1 > len(client.cards_in_hand):
            message.success = False
            if len(client.cards_in_hand) < 1:
                message.message = "Cards in hand is empty"
            else :
                message.message = "Card's number not valid"
            message = pickle.dumps(message)
            new_message_header = MessageHeader.make_header(
                MessageType.Ingame,
                client.username,
                len(message),
                'server'
            )
        else:
            card = client.cards_in_hand[message.card_number_1 - 1]
            opponent = Room.search_for_opponent(client)

            client.cards_in_hand.remove(card)
            client.cards_in_field.append(card)

            opponent.state = ClientState.Playing
            client.state = ClientState.WaitForTurn

            IngameRepository.send_opponent_message(client, "Now Your Turn")

            message.success = True
            message.message = "Success drawing card"
            message = pickle.dumps(message)
            new_message_header = MessageHeader.make_header(
                MessageType.Ingame,
                client.username,
                len(message),
                'server'
            )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_attack(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])
        ingame_message = receive_message(client.client, message_size)
        ingame_message = pickle.loads(ingame_message)
        new_message_header = None

        opponent = Room.search_for_opponent(client)

        if len(client.cards_in_field) < 1 or \
            len(opponent.cards_in_field) < 1 or \
            ingame_message.card_number_1 > len(client.cards_in_field) or \
            ingame_message.card_number_2 > len(opponent.cards_in_field) :
            ingame_message.success = False
            if len(client.cards_in_field) < 1:
                ingame_message.message = "Cards in own field is empty"
            elif len(opponent.cards_in_field) < 1 :
                ingame_message.message = "Card in opponent field is empty"
            elif ingame_message.card_number_1 - 1 > len(client.cards_in_field):
                ingame_message.message = "The attacker card's number is wrong"
            else :
                ingame_message.message = "The attacked card's number is wrong"
            ingame_message = pickle.dumps(ingame_message)
            new_message_header = MessageHeader.make_header(
                MessageType.Ingame,
                client.username,
                len(ingame_message),
                'server'
            )
        else:
            message = ""
            attacker_card = client.cards_in_field[ingame_message.card_number_1 - 1]
            attacked_card = opponent.cards_in_field[ingame_message.card_number_2 - 1]

            message += "{}'s {} attacked by {}'s {}\n".format(opponent.username, attacked_card.name, client.username, attacker_card.name)
            message += "{}'s {} defence reduced by {}\n".format(opponent.username, attacked_card.name, attacker_card.attack)

            if attacker_card.attack <= attacked_card.defence:
                attacker_card.defence -= attacked_card.attack
                message += "{}'s {} defence reduced by {}\n".format(client.username, attacker_card.name, attacked_card.attack)

            attacked_card.defence -= attacker_card.attack

            message = IngameRepository.filter_died_card(client, message)
            message = IngameRepository.filter_died_card(opponent, message)

            finished = False

            if IngameRepository.check_if_lose(client) and IngameRepository.check_if_lose(opponent):
                User.add_point_for_user(client.username, 25)
                User.add_point_for_user(opponent.username, 25)

                message = "The game result is Draw!!! Everyone got 25 points"
                finished = True
            elif IngameRepository.check_if_lose(client):
                User.add_point_for_user(opponent.username, 50)

                message = "{} win!!{} got 50 points".format(opponent.username, opponent.username)
                finished = True
            elif IngameRepository.check_if_lose(opponent):
                User.add_point_for_user(client.username, 50)
                message = "{} win!!{} got 50 points".format(client.username, client.username)
                finished = True
                
            IngameRepository.send_opponent_message(client, message, finished=finished)

            if finished :
                client.state = ClientState.Menu
                opponent.state = ClientState.Menu
                Room.delete_room(client)
            else :
                client.state = ClientState.WaitForTurn
                opponent.state = ClientState.Playing


            ingame_message.success = True
            ingame_message.message = message
            ingame_message.finished = finished
            ingame_message = pickle.dumps(ingame_message)
            new_message_header = MessageHeader.make_header(
                MessageType.Ingame,
                client.username,
                len(ingame_message),
                'server'
            )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, ingame_message)
