from models.user import User
from models.user_card import UserCard
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
import pickle
import settings

class RegisterRepository:
    card_for_new_member = [1, 2, 19, 20, 21]

    @staticmethod
    def handle(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        register_message = pickle.loads(message)

        result = User.get_user_by_username(register_message.username)

        if len(result) > 0:
            register_message.success = False
            register_message.message = "Username already been taken"
            message = pickle.dumps(register_message)
            new_message_header = MessageHeader.make_header(
                MessageType.Register,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        user = User(
            register_message.username,
            register_message.password,
            100,
            "",
            0
        )
        session.add(user)
        session.commit()

        user = User.get_user_by_username(register_message.username)[0]

        for card in RegisterRepository.card_for_new_member:
            user_card = UserCard(
                user.id,
                card
            )

            session.add(user_card)

            user_card = UserCard(
                user.id,
                card
            )

            session.add(user_card)
        session.commit()

        user = User.get_user_by_username(register_message.username)[0]

        client.username = register_message.username
        client.state = ClientState.Menu

        register_message.success = True
        register_message.message = "Register success!!"
        message = pickle.dumps(register_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Register,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
