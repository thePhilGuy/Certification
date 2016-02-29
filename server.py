import socket, ssl

def handle_client(ssl_socket):
    print ssl_socket.recv(100)

# Create underlying listening socket
s = socket.socket()
s.bind(('', 10023))
s.listen(1)

try:
    while True:
        # Accept client connection with SSL certificate
        connection, fromaddr = s.accept()
        ssl_socket = ssl.wrap_socket(connection,
                                     server_side=True,
                                     certfile="server.crt",
                                     keyfile="server.key",
                                     ca_certs="client.crt",
                                     cert_reqs=ssl.CERT_REQUIRED)
        try:
            handle_client(ssl_socket)
        finally:
            ssl_socket.shutdown(socket.SHUT_RDWR)
            ssl_socket.close()
except KeyboardInterrupt:
    sys.exit("Server interrupted by keyboard.")
