import socket as sk
import time
import os
import threading
import pickle
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
        # Insertion of packets in the list
        file_packets.append(chunk)
        i = i + 1

    # Make the header message
    num_packets = len(file_packets)
    message = '%s'% num_packets

    # Send header file
    while True:
        try: 
            sock.sendto(message.encode(), address)
            # Catch server response
            response = sock.recvfrom(4096).decode()
        except Exception:
            sock.sendto(message.encode(), address)

        if response == 'Header arrived':
            break

    # Start uploading 
    print('Uploading..')
    for packet in file_packets :
        sock.sendto(pickle.dumps(packet), address) 
    
    while True:
        # It manage server ACK for upload ending
        try:
            response = sock.recvfrom(4096).decode()
            # code 200 : Upload Succesful
            if response == '200':
                print('Upload finished')
                return 
            # code 111 : server ask packets again
            elif response == '111':
                for packet in file_packets :
                    sock.sendto(pickle.dumps(packet), address) # It might throw exceptions
            else:
                print('Upload failed')
                return
        except Exception:
            print('Upload failed')
            return


def __download__(sock, filename, address):
    # Create a new file 
    packet = open(filename, 'w')
    # Receive packet from server and write to the file
    data, address = sock.recvfrom(PACKET_SIZE_DOWNLOAD)
    packet.write(data.decode('utf8'))

    packet.close()
    # Send a packet
    print("Finished!")