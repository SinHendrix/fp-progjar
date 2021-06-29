from models.user import User
from models.user_card import UserCard
from models.card import Card
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
import pickle
import settings

class ShopRepository:
    @staticmethod
    def handle_check_shop(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        check_shop_message = receive_message(client.client, message_size)
        check_shop_message = pickle.loads(check_shop_message)

        cards = session.query(Card).all()
        message = ""

        for card in cards:
            message += "{}. {}\nAttack : {}\nDefence : {}\nPrice : {}\n".format(card.id, card.name, card.attack, card.defence, card.price)

        check_shop_message.success = True
        check_shop_message.message = message
        message = pickle.dumps(check_shop_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Shop,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_check_point(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        check_point_message = receive_message(client.client, message_size)
        check_point_message = pickle.loads(check_point_message)

        user = User.get_user_by_username(client.username)[0]
        message = "Your point is {}".format(user.points)

        check_point_message.success = True
        check_point_message.message = message
        message = pickle.dumps(check_point_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Shop,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_buy(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        buy_card_message = receive_message(client.client, message_size)
        buy_card_message = pickle.loads(buy_card_message)

        result = session.query(Card).filter_by(id=buy_card_message.card).all()
        user = User.get_user_by_username(client.username)[0]

        if len(result) < 1 or result[0].price > user.points:
            buy_card_message.success = False
            if len(result) < 1:
                buy_card_message.message = "Card not found"
            else :
                buy_card_message.message = "Point not enough"
            message = pickle.dumps(buy_card_message)
            new_message_header = MessageHeader.make_header(
                MessageType.Shop,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        user_card = UserCard(
            user.id,
            buy_card_message.card
        )

        session.add(user_card)

        session.query(User).filter_by(id=user.id).update({"points":user.points - result[0].price})
        session.commit()

        buy_card_message.success = True
        buy_card_message.message = "Buy success!!"
        message = pickle.dumps(buy_card_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Shop,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
