import socket #importeer socket module
import time #importeer tijd module
import sys #importeer sys module

from sys import argv #importer argv
from cryptography.fernet import Fernet #importer fernet
from cryptography.fernet import InvalidToken #importeer exceptionerror

try: #executeer
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #maak UDP socket
  host = ('127.0.0.1', 7777) #maak local host en poort

except socket.error as error: #vang exception error op
  print('Socket aanmaken mislukt')
  sys.exit() #sluit programma

with open(sys.argv[1], "rt") as contents: #open 1e file in readtext als content
   for eachline in contents: #voor elke regel in contents
     message = eachline # message[eachline]
     print('verstuurde bericht',message)
     message = message.encode() #verander tekst naar binary
     key = '2XPvZBLrbZ1kOSDjH78CvZQgygP1BvCFmntgQLWqTzQ=' #maak sym key
     f = Fernet(key) #wijs key toe
     message = f.encrypt(message) #encrypt message
     #print('Ge-encrypted ', message)

     sent = sock.sendto(message, host) #stuur data naar server
     time.sleep(1) #wacht 1 sec na zenden

while 1: #voor data ontvangen
  data, address = sock.recvfrom(4096) #ontvang data van client sock met max 4096 bytes
  time.sleep(1) #wacht na ontvangen 1 sec

  try: #executeer
    key = '2XPvZBLrbZ1kOSDjH78CvZQgygP1BvCFmntgQLWqTzQ=' #maak symetrische sleutel
    f = Fernet(key) # wijs key toe
    decrypted = f.decrypt(data) #decrypt data
    data = decrypted.decode() #verander van binary naar string

  except InvalidToken as wrongkey: #vang exception op
    print('Foute key')
    sys.exit() #sluit programma af

  a = data #wijs data toe aan a
  print('ontvangen',a)

  file = open(sys.argv[2], "a") # open 2e file in append mode
  file.write(a) #schrijf decoded data naar a
  file.close() #sluit bestand