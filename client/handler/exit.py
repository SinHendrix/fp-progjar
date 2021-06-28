import sys
import settings

def client_exit(sock_cli):
    sock_cli.send(bytes("|".join(['exit', "\n\n\n\n"]), settings.ENCODING))
    sock_cli.close()
    sys.exit()
