import socket, ssl, sys, base64, os
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

def put_file(filename, hashed, size, ssl_socket):
    contents = recvb64(ssl_socket, size)
    with open('recv/'+filename, 'w') as ofile:
        # Write plaintext to file
        ofile.write(contents)
    with open('recv/'+filename+'.sha256', 'w') as hashfile:
        # Write hash to file
        hashfile.write(hashed)
    print filename, "written to file."

def get_file(filename, ssl_socket):
    file_exists = os.path.isfile('recv/'+filename) and os.path.isfile('recv/'+filename+'.sha256')
    if file_exists:
        content = ""
        try:
            # Read and send Hash file
            hfile = open('recv/'+filename+'.sha256', 'r')
            hashed_content = hfile.read()
            ssl_socket.write(hashed_content)
            hfile.close()
            # Read and send content file
            ifile = open('recv/'+filename, 'r')
            content = base64.b64encode(ifile.read())
            ssl_socket.write("Size: " + str(len(content)))
            ssl_socket.write(content)
            ifile.close()
            print filename, "sent to client"
        except:
            ssl_socket.write("Failure: File could not be retrieved.")
    else:
        print "File does not exist."
        ssl_socket.write("Failure: File could not be retrieved.")

def handle_client(ssl_socket):
    command = ssl_socket.recv(4)
    if command == "stop":
        # Stop handling this client
        return False
    filename = ssl_socket.recv(100)[10:]
    if command == "put":
        # Download file from client
        hashed = ssl_socket.recv(100)[6:]
        f_size = int(ssl_socket.recv(100)[6:])
        put_file(filename, hashed, f_size, ssl_socket)
    elif command == "get":
        # Send file to client
        get_file(filename, ssl_socket)
    else:
        # Somehow received an invalid command
        sys.exit("/!\\ Received command that is neither put, get, or stop.")
    return True

# Parse command line args
if len(sys.argv) != 2:
    sys.exit("Usage: python server.py port")
try:
    port = int(sys.argv[1])
    if port < 0 or port > 65536:
        raise ValueError()
except:
    sys.exit("Port must be a positive integer <= 65536")

# Create underlying listening socket
s = socket.socket()
s.bind(('', port))
s.listen(1)

try:
    # Accept client connection with SSL certificate
    connection, fromaddr = s.accept()
    ssl_socket = ssl.wrap_socket(connection,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ca_certs="client.crt",
                                 cert_reqs=ssl.CERT_REQUIRED)
    running = True
    while running:
        running = handle_client(ssl_socket)
except KeyboardInterrupt:
    sys.exit("Server interrupted by keyboard.")
finally:
    if "ssl_socket" in locals():
        ssl_socket.shutdown(socket.SHUT_RDWR)
        ssl_socket.close()
    s.close()
