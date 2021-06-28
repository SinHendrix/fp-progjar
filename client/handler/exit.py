import settings
import sys
from classes.message_type import MessageType

def client_exit(message_receiver):
    message_receiver.client.send(bytes("|".join([MessageType.Exit, "\n\n\n\n"]), settings.ENCODING))
    message_receiver.client.close()
    message_receiver.raise_exception()
    sys.exit()
