import socket as sk
import time
import os

PACKET_SIZE_UPLOAD = 32768
PACKET_SIZE_DOWNLOAD = 65536

def __upload__(sock, filename, address):
    filesize = os.path.getsize(filename)
    file_packets = []
    file = open(filename, 'rb')
    while True:
        # Read bytes from the file
        packet = file.read(PACKET_SIZE_UPLOAD)
        # If bytes_read not read any bytes file transfer is finished
        if not packet:
            file.close()
            break
    
         # Isertion of packets in the list 
        file_packets.append(packet)
        # Send a packet
        #sock.sendto(packet, address)

    print(file_packets)


def __download__(sock, filename, address):
    # Create a new file 
    packet = open(filename, 'w')
    # Receive packet from server and write to the file
    data, address = sock.recvfrom(PACKET_SIZE_DOWNLOAD)
    packet.write(data.decode('utf8'))
    packet.close()
    # Send a packet
    print("Finished!")

