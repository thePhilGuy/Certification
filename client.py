import socket, ssl, pprint
from mycrypto import *

class Client:
    def __init__(self, server_host, server_port):
        # Connect to server, create tls socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_socket = ssl.wrap_socket(s,
                                          certfile="client.crt",
                                          keyfile="client.key",
                                          ca_certs="server.crt",
                                          cert_reqs=ssl.CERT_REQUIRED)
        self.ssl_socket.connect((server_host, server_port))
        self.ssl_socket.write("I have established myself in the server!")

    def __del__(self):
        # Close socket when done with this object
        self.ssl_socket.close()

    def put(self, tokens):
        # Put file onto server
        # Verify 3 parameters
        if (len(tokens)) != 3:
            print "Usage: put filepath E|N"
        else:
            try:
                # Open file to send
                putfile = open(tokens[1], 'r')
                plaintext = putfile.read()
                putfile.close()

                # Send file to Server
                

            except:
                print "/!\\ File", tokens[1], "cannot be sent."
        return True

    def get(self, tokens):
        print "getting ", tokens[1:]
        return True

    def exit(self, _):
        return False

# ==============================================================================
# Connect ssl socket to server
client = Client('localhost', 10023)

# ==============================================================================
options = {
    "put": Client.put,
    "get": Client.get,
    "exit": Client.exit
}

running = True
while running:
    tokens = raw_input("Please enter your command: ").split()
    try:
        running = options[tokens[0]](client, tokens)
    except KeyError:
        print "/!\\ Invalid command /!\\. Please use put, get, or exit."
