import socket #importeer socket module
import sys #importeer sys module
from cryptography.fernet import Fernet #importeer fernet module
from cryptography.fernet import InvalidToken #importeer exception error

try: #executeer
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #maak UDP socket
    host = ('127.0.0.1', 7777) #maak local host en poort

except socket.error as error: #vang exception error op
    print('Socket aanmaken mislukt')
    sys.exit() #programma afsluiten

try: #executeer
    sock.bind(host) #bind ip en poort aan socket

except socket.error as error: #exception error opvangen
    print('Bind is mislukt')
    sys.exit()

while 1: #alleen voor ontvangen
    data, address = sock.recvfrom(4096) #accepteer hoeveelheid bytes

    try:
        key = '2XPvZBLrbZ1kOSDjH78CvZQgygP1BvCFmntgQLWqTzQ=' #maak symetrische sleutel
        f = Fernet(key) #wijs key toe
        decrypted = f.decrypt(data) #decrypt data
        print('Decrypted data', data)
        data = decrypted.decode() #verander binary naar string

    except InvalidToken as wrongkey: #als de key niet overeenkomt
        print('Foute key')
        sys.exit() #sluit programma af

    data = data.upper() #maak hoofdletters van data

    if data: #als er data is
        data = data.encode() #verander string naar binary
        key = '2XPvZBLrbZ1kOSDjH78CvZQgygP1BvCFmntgQLWqTzQ='
        f = Fernet(key) #wijs key toe
        data = f.encrypt(data) #encrypt data

        #print('Server ge-encrypted', data)
        sent = sock.sendto(data, address) #stuur data naar client
        print('De verstuurde berichten', data)

