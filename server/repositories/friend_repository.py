from models.user import User
from models.relationship import Relationship
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
import pickle
import settings

class FriendRepository:
    @staticmethod
    def handle_add_friend(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        add_friend_message = pickle.loads(message)

        result = session.query(User).filter_by(
            username=add_friend_message.friend_username
        ).all()

        if len(result) < 1:
            add_friend_message.success = False
            add_friend_message.message = "User not found"
            message = pickle.dumps(add_friend_message)
            new_message_header = MessageHeader.make_header(
                MessageType.AddFriend,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        friend_user = result[0]
        user = session.query(User).filter_by(
            username=client.username
        ).all()[0]

        relationship = session.query(Relationship).filter_by(
            user_id_1=friend_user.id,
            user_id_2=user.id
        ).all()

        if len(relationship) > 1:
            add_friend_message.success = False
            add_friend_message.message = "User already a friend"
            message = pickle.dumps(add_friend_message)
            new_message_header = MessageHeader.make_header(
                MessageType.AddFriend,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        relationship_1 = Relationship(
            user.id,
            friend_user.id
        )
        relationship_2 = Relationship(
            friend_user.id,
            user.id
        )

        session.add(relationship_1)
        session.add(relationship_2)

        add_friend_message.success = True
        add_friend_message.message = "Add Friend success!!"
        message = pickle.dumps(add_friend_message)
        new_message_header = MessageHeader.make_header(
            MessageType.AddFriend,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)

    @staticmethod
    def handle_list_friend(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        list_friend_message = pickle.loads(message)

        user = session.query(User).filter_by(
            username=client.username
        ).all()[0]

        relationships = session.query(Relationship).filter_by(
            user_id_1=user.id
        ).all()

        if len(relationships) < 1:
            list_friend_message.success = False
            list_friend_message.message = "You don't have any friend yet"
            message = pickle.dumps(list_friend_message)
            new_message_header = MessageHeader.make_header(
                MessageType.ListFriend,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        friend_list = ""

        for relationship in relationships:
            friend = session.query(User).filter_by(
                id=relationship.user_id_2
            ).all()[0]

            friend_list += "- " + friend.username + "\n"


        list_friend_message.success = True
        list_friend_message.message = friend_list
        message = pickle.dumps(list_friend_message)
        new_message_header = MessageHeader.make_header(
            MessageType.ListFriend,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
