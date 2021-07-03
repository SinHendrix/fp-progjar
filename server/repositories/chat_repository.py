from models.user import User
from models.relationship import Relationship
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
from sqlalchemy import func
import pickle
import settings

class ChatRepository:
    @staticmethod
    def send_message_to_user(client, username, message, file_name="", is_file=False):
        for person in client.clients:
            if person.username == username:
                new_message_header = MessageHeader.make_header(
                    MessageType.File if is_file else MessageType.Message,
                    username,
                    len(message),
                    client.username,
                    file_name=file_name
                )

                send_message(person.client, bytes(new_message_header, settings.ENCODING))
                send_message(person.client, message)
                return

    @staticmethod
    def handle_text_message(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        text_message = receive_message(client.client, message_size)

        if message_header[MessageHeader.destination] == 'bcast':
            user_client = User.get_user_by_username(client.username)[0]
            relationships = session.query(Relationship).filter_by(
                user_id_1=user_client.id
            ).all()

            for relationship in relationships:
                user = User.get_user_by_id(relationship.user_id_2)[0]

                ChatRepository.send_message_to_user(client, user.username, text_message)
        else :
            if Relationship.check_if_friend(client.username, message_header[MessageHeader.destination]):
                ChatRepository.send_message_to_user(client, message_header[MessageHeader.destination], text_message)

    @staticmethod
    def handle_file_message(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        file_message = receive_message(client.client, message_size)

        if message_header[MessageHeader.destination] == 'bcast':
            user_client = User.get_user_by_username(client.username)[0]
            relationships = session.query(Relationship).filter_by(
                user_id_1=user_client.id
            ).all()

            for relationship in relationships:
                user = User.get_user_by_id(relationship.user_id_2)[0]

                ChatRepository.send_message_to_user(
                    client,
                    user.username,
                    file_message,
                    file_name=ssage_header[MessageHeader.file_name],
                    is_file=True
                )
        else :
            if Relationship.check_if_friend(client.username, message_header[MessageHeader.destination]):
                ChatRepository.send_message_to_user(
                    client,
                    message_header[MessageHeader.destination],
                    file_message,
                    file_name= message_header[MessageHeader.file_name],
                    is_file=True
                )
