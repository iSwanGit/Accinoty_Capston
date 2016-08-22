# -*- coding: utf8 -*-
import sys
import socket
import json

class SendProcessor:
    HOST = "accinoty.pendual.net"
    PORT = 8088
    BUFSIZE = 1024
    ADDR = (HOST, PORT)



HOST= "accinoty.pendual.net"
PORT= 8088
BUFSIZE= 1024
ADDR= (HOST, PORT)

# Making Enum
def enum(**named_values):
    return type('Enum', (), named_values)

Status= enum(IDLE= 0, OCCUR= 1, AROUND= 2)


#### TEST DATA ####
latitude= 36.0
longitutde= 126.0
curStatus= Status.IDLE
carIndex= '14허 3810'
receivedIndex= '69호 5366' #주변의 사고차량 번호
##################

jsonObj= {
    'type': curStatus,
    'car_index': carIndex,
    #'accident_around': receivedIndex,
    # packet type
    'latitude': latitude,
    'longitude': longitutde,
}
jsonString= json.dumps(jsonObj)
jsonLength= len(jsonString)


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.connect(ADDR)
    print('Connected to server successfully')
except Exception as e:
    print('Cannot connect server')
    sys.exit()


mySocket.send(jsonString.encode())


#print(repr(recvData))

# TODO: socket, json?multisend?, thread

