import socket as sk
import time
import os
import threading
from packet import Packet

PACKET_SIZE_UPLOAD = 32768
PACKET_SIZE_DOWNLOAD = 65536

def __upload__(sock, filename, address):

    filesize = os.path.getsize(filename)
    i = 1
    file_packets = []
    file = open(filename, 'rb')
    while True:
        # Read bytes from the file
        packet_body = file.read(PACKET_SIZE_UPLOAD)
        # If bytes_read not read any bytes file transfer is finished
        if not packet_body:
            file.close()
            break
        chunk = Packet(i, packet_body)
        # Isertion of packets in the list 
        file_packets.append(chunk)
        i = i + 1

    # Make the header message
    num_packets = len(file_packets)
    message = '{num_packets}, {filesize}'

    # Send header file
    try: 
        while True:
            sock.sendto(message, address)
    except Exception as info:
        sock.sendto(message, address)

    # Catch server response
    response = sock.recvfrom(4096)

    if response == 'Header arrived':
        print(response) #print a caso per non dare problemi
        # Inizio a creare thread per inviare i pacchetti


def __download__(sock, filename, address):
    # Create a new file 
    packet = open(filename, 'w')
    # Receive packet from server and write to the file
    data, address = sock.recvfrom(PACKET_SIZE_DOWNLOAD)
    packet.write(data.decode('utf8'))
    packet.close()
    # Send a packet
    print("Finished!")

