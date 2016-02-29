import socket, ssl, sys, base64
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
        # self.ssl_socket.write("I have established myself in the server!")

    def __del__(self):
        # Close socket when done with this object
        self.ssl_socket.close()

    def put(self, tokens):
        # Put file onto server
        # Verify 3 parameters
        if (len(tokens)) != 3:
            print "Usage: put filepath E|N"
        else:
            # try:
                # Open file to send
                putfile = open(tokens[1], 'r')
                plaintext = putfile.read()
                putfile.close()

                # Send file to Server
                encoded_text = base64.b64encode(plaintext)
                length = len(encoded_text)
                self.ssl_socket.write("put")
                self.ssl_socket.write("Filename: " + tokens[1])
                self.ssl_socket.write("Size: " + str(length))
                self.ssl_socket.write(encoded_text)
            # except:
            #     print "/!\\ File", tokens[1], "cannot be sent."
        return True

    def get(self, tokens):
        print "getting ", tokens[1:]
        return True

    def stop(self, _):
        self.ssl_socket.write("stop")
        return False

# ==============================================================================
# Parse command line args
if len(sys.argv) != 3:
    sys.exit("Usage: python client.py server_hostname port")
try:
    port = int(sys.argv[2])
    if port < 0 or port > 65536:
        raise ValueError()
except:
    sys.exit("Port must be a positive integer <= 65536")

try:
    hostname = sys.argv[1]
    # Connect ssl socket to server
    client = Client(hostname, port)
except:
    sys.exit("Connection refused.")

# ==============================================================================
options = {
    "put": Client.put,
    "get": Client.get,
    "stop": Client.stop
}

running = True
while running:
    tokens = raw_input("Please enter your command: ").split()
    try:
        running = options[tokens[0]](client, tokens)
    except KeyError:
        print "/!\\ Invalid command /!\\. Please use put, get, or exit."
