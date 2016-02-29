import socket, ssl, pprint
from mycrypto import *

def put(tokens):
    # Verify 3 parameters
    if (len(tokens)) != 3:
        print "Usage: put filepath E|N"
    else:
        try:
            # Open file to send
            putfile = open(tokens[1], 'r')
            plaintext = putfile.read()
            putfile.close()
            print plaintext
        except:
            print "/!\\ File", tokens[1], "cannot be sent."
    return True

def get(tokens):
    print "getting ", tokens[1:]
    return True

def exit(_):
    return False
# ==============================================================================
# Connect ssl socket to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = ssl.wrap_socket(s,
                             certfile="client.crt",
                             keyfile="client.key",
                             ca_certs="server.crt",
                             cert_reqs=ssl.CERT_REQUIRED)
ssl_socket.connect(('localhost', 10023))

ssl_socket.write("I have established myself in the server!")
print pprint.pformat(ssl_socket.getpeercert())
ssl_socket.close()

# ==============================================================================
options = {
    "put": put,
    "get": get,
    "exit": exit
}

running = True
while running:
    tokens = raw_input("Please enter your command: ").split()
    try:
        running = options[tokens[0]](tokens)
    except KeyError:
        print "/!\\ Invalid command /!\\. Please use put, get, or exit."
