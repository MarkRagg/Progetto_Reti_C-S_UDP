import socket as sk
import os
import pickle
from packet import Packet
import hashlib

PACKET_SIZE_UPLOAD = 32768
PACKET_SIZE_DOWNLOAD = 65536

download_path = os.getcwd()+"\\Download\\"

def __upload__(sock, filename, address):

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
            response, addr = sock.recvfrom(4096)
        except sk.error:
            sock.sendto(message.encode(), address)
            
        if response.decode() == 'Header arrived':
            break

    # Start uploading 
    print('Uploading..')
    for packet in file_packets :
        print("Send packet n. %s" % packet.packet_number)
        a = pickle.dumps(packet)
        sock.sendto(a, address) 
    
    while True:
        # It manage server ACK for upload ending
        try:
            response, addr = sock.recvfrom(4096)
            response = response.decode()
            # code 200 : Upload Successful
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
        except sk.error:
            print('Upload failed')
            return

def __download__(sock, filename, address):
    while True:
        data, addr = sock.recvfrom(4096)
        print ("File name: %s" % filename)
        file_msg = data

        f = open(filename, 'wb')

        # server send the number of packets in the file to the client
        n_packet = file_msg
        print("Number of packets %s" % n_packet.decode())
        x = "Header arrived"
        sock.sendto(x.encode(), addr)
        
        i = 0
        
        # list for all packets received from server
        packets = []
      
        while i < int(n_packet.decode()):
            try:
                data, addr = sock.recvfrom(PACKET_SIZE_DOWNLOAD)    
                data_enc  = pickle.loads(data)
                checksum = hashlib.md5(data_enc.body).digest()
                if checksum != data_enc.checksum:
                    print("Checksum error")
                    i = 0
                    msg = "111"      
                    packets.clear()
                    sock.sendto(msg.encode(), addr)
                    continue 
                i = i+1
                # add the data received from server to the list
                print("Put in the list packet")
                packets.append(data_enc)
            except sk.error as err:
                print(err)
                i = 0
                msg = "111"      # 111 : something went wrong
                packets.clear()
                sock.sendto(msg.encode(), addr)
                
        # 200 : all packet arrived
        if len(packets) == int(n_packet.decode()):
            msg = "200"
            sock.sendto(msg.encode(), addr)
            packets.sort(key=lambda x: x.packet_number)
            
            for packet in packets:     
                f.write(packet.body)
            print ("%s finish!" % filename)
            break             
    f.close()