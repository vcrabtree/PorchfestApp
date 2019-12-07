#just to remove slashes

def encode(string):
    string.replace('/', '%3')

def decode(string):
    string.replace('%3', '/')