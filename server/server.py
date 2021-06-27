sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("0.0.0.0", settings.port))
sock_server.listen(5)

clients = []
