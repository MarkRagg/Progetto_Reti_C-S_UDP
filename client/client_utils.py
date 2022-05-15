import socket as sk
import time
import os

def __upload__(sock, filename, address):
    filesize = os.path.getsize(filename)
    print(filename)
    packet = open(filename, 'rb')
    while True:
        # Read bytes from the file
        bytes_read = packet.read(filesize)
        # If bytes_read not read any bytes file transfer is finished
        if not bytes_read:
            packet.close()
            break
        # Send a packet
        sock.sendto(bytes_read, address)


def __download__(sock, filename, address):
    # Create a new file 
    packet = open(filename, 'w')
    # Receive packet from server and write to the file
    data, address = sock.recvfrom(4096)
    packet.write(data.decode('utf8'))
    packet.close()
    # Send a packet
    print("Finished!")

