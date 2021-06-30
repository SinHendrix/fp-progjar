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
    def send_opponent_message(client, message):
        opponent = Room.search_for_opponent(client)
        opponent.state = ClientState.Playing
        ingame_message = IngameMessage(0)
        ingame_message.success = True
        ingame_message.message = message
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
    def handle_draw_card(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])
        message = receive_message(client.client, message_size)
        message = pickle.loads(message)
        new_message_header = None

        if len(client.cards_in_hand) < 1 or message.card_number_1 - 1 > len(client.cards_in_hand):
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
            client.cards_in_hand.remove(card)
            client.cards_in_field.append(card)

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
