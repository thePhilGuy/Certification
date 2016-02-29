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
