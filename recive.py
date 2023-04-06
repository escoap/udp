import socket


localIP = "172.20.10.4"
localPort = 3520
bufferSize = 202400

UDPSock = socket.socket(family = socket.AF_INET,type = socket.SOCK_DGRAM) #Socket Datagram
UDPSock.bind((localIP,localPort))
print("Socket running and listening")
run = 1
while run==1:
    bytesaddypair = UDPSock.recvfrom(bufferSize)
    message = bytesaddypair[0]
    addy = bytesaddypair[1]
    print(message)
    print(addy)
    run = int(input("1 or 2"))