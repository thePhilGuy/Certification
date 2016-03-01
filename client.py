import socket, ssl, sys, base64
from mycrypto import *

def recvb64(sock, length):
    # Recv long files
    buffer = ""
    if length > 4096:
        while length > 4096:
            buffer += base64.b64decode(sock.recv(4096))
            length -= 4096
        buffer += base64.b64decode(sock.recv(length))
    else:
        buffer += base64.b64decode(sock.recv(length))
    return buffer

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
        encrypt = False
        # Verify parameters
        if len(tokens) != 3 and len(tokens) != 4:
            print "Usage: put filepath N|[E [password]]"
        elif len(tokens) == 3 and tokens[2] != 'N':
            print "Client expects flag N for normal mode. ( 2 params to put)"
        elif len(tokens) == 4 and (tokens[2] != 'E' or len(tokens[3]) != 8):
            print "Client expects flag E for encrypted mode as well as an 8 character password."
        else:
            encrypt = tokens[2] == 'E'
            try:
                # Open file to send
                putfile = open(tokens[1], 'r')
                plaintext = putfile.read()
                putfile.close()

                encoded_text = ''
                hashed_text = SHA256_hash(plaintext)
                if encrypt:
                    password = tokens[3]
                    key = SHA256_hash(password)[:16]
                    ciphertext = AES_encrypt(plaintext, key)
                    encoded_text = base64.b64encode(ciphertext)
                else:
                    encoded_text = base64.b64encode(plaintext)

                # Send file to Server
                length = len(encoded_text)
                self.ssl_socket.write("put")
                self.ssl_socket.write("Filename: " + tokens[1])
                self.ssl_socket.write("Hash: " + hashed_text)
                self.ssl_socket.write("Size: " + str(length))
                self.ssl_socket.write(encoded_text)
                print tokens[1], "sent to server."
            except:
                print "/!\\ File", tokens[1], "cannot be sent."
        return True

    def get(self, tokens):
        # Get from from Server
        encrypt = False
        # Verifiy parameters
        if len(tokens) != 3 and len(tokens) != 4:
            print "Usage: get filepath N|[E [password]]"
        elif len(tokens) == 3 and tokens[2] != 'N':
            print "Client expects flag N for normal mode. ( 2 params to get)"
        elif len(tokens) == 4 and (tokens[2] != 'E' or len(tokens[3]) != 8):
            print "Client expects flag E for encrypted mode as well as an 8 character password."
        else:
            encrypt = tokens[2] == 'E'
            filename = tokens[1]
            # Good params, request the file from the server
            self.ssl_socket.write("get")
            self.ssl_socket.write("Filename: " + filename)

            # Receive response
            hashed = self.ssl_socket.recv(64)
            if hashed[:7] == "Failure:":
                print hashed
                return True
            size = int(self.ssl_socket.recv(100)[6:])
            content = recvb64(self.ssl_socket, size)

            # Decrypt if necessary
            plaintext = ''
            if encrypt:
                password = tokens[3]
                key = SHA256_hash(password)[:16]
                plaintext = AES_decrypt(content, key)
            else:
                plaintext = content

            # Verify that file matches hash
            if hashed != SHA256_hash(plaintext):
                print "/!\\ Verification failed: file does not match hash"
                return True

            # Write response to file
            try:
                ofile = open(filename, 'w')
                ofile.write(plaintext)
                ofile.close()
                print filename, "written to file."
            except:
                print "/!\\ File", filename, "could not be written."
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

options = {
    "put": Client.put,
    "get": Client.get,
    "stop": Client.stop }

running = True
while running:
    tokens = raw_input("Please enter your command: ").split()
    try:
        running = options[tokens[0]](client, tokens)
    except KeyError, IndexError:
        print "/!\\ Invalid command /!\\. Please use put, get, or exit."
