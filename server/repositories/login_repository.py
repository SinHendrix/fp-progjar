from models.user import User
from models.base import session
from utils.message import receive_message, send_message
from classes.message_header import MessageHeader
from classes.message_type import MessageType
from classes.client_state import ClientState
import pickle
import settings

class LoginRepository:
    @staticmethod
    def handle(client, message_header):
        message_size = int(message_header[MessageHeader.message_size])

        message = receive_message(client.client, message_size)
        login_message = pickle.loads(message)

        result = session.query(User).filter_by(
            username=login_message.username,
            password=login_message.password
        ).all()

        if len(result) < 1:
            login_message.success = False
            login_message.message = "User not found"
            message = pickle.dumps(login_message)
            new_message_header = MessageHeader.make_header(
                MessageType.Register,
                client.username,
                len(message),
                'server'
            )
            send_message(client.client, bytes(new_message_header, settings.ENCODING))
            send_message(client.client, message)
            return

        client.username = login_message.username
        client.state = ClientState.Menu

        login_message.success = True
        login_message.message = "Login success!!"
        message = pickle.dumps(login_message)
        new_message_header = MessageHeader.make_header(
            MessageType.Login,
            client.username,
            len(message),
            'server'
        )

        send_message(client.client, bytes(new_message_header, settings.ENCODING))
        send_message(client.client, message)
