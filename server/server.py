'''
                            UDP SERVER SOCKET
Dilaver Shtini
'''

import socket as sk
import os
#import time
import pickle
from packet import Packet
import hashlib


PACKET_SIZE_UPLOAD = 32768
PACKET_SIZE_DOWNLOAD = 65536

#path to get files
path = os.getcwd()+"\\file"

resp = ""

# create the socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Download files from server to client
def download(file_name, address):

    i = 1
    file_packets = []
    file = open(path+"\\"+file_name, 'rb')
    while True:
        # Read bytes from the file
        packet_body = file.read(PACKET_SIZE_UPLOAD)
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
            # Catch client response
            response, addr = sock.recvfrom(4096)
        except sk.error:
            sock.sendto(message.encode(), address)
            
        if response.decode() == 'Header arrived':
            break

    # Start downloading 
    print('Downloading...')
    for packet in file_packets :
        print("Send packet n. %s" % packet.packet_number)
        a = pickle.dumps(packet)
        sock.sendto(a, address) 
    
    while True:
        try:
            response, addr = sock.recvfrom(4096)
            response = response.decode()
            # code 200 : Download Successful
            if response == '200':
                print('Download finished')
                return 
            # code 111 : client ask packets again
            elif response == '111':
                for packet in file_packets :
                    sock.sendto(pickle.dumps(packet), address) # It might throw exceptions
            else:
                print('Download failed')
                return
        except sk.error:
            print('Download failed')
            return
    
# Upload files from client to server
def upload(file_name):    
    
    while True:
        data, addr = sock.recvfrom(4096)
        if data:
            print ("File name: %s" % file_name)
            file_msg = data
            
        # create the new file on the server without content
        new_path = path+"\\"+file_name
        f = open(new_path, 'wb')

        # client send the number of packets in the file to the server
        n_packet = file_msg
        print("Number of packets %s" % n_packet.decode())
        x = "Header arrived"
        sock.sendto(x.encode(), addr)
        
        # now i can receive the data from the client
        i = 0
        
        # list for all packets received from client
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
                    sock.sendto(msg, addr)
                    continue 
                i = i+1
                # add the data received from client to the list
                print("Put in the list")
                packets.append(data_enc)
            except Exception as error:
                print(error)
                i = 0
                msg = "111"      # 111 : something went wrong
                packets.clear()
                sock.sendto(msg.encode(), addr)

        # 200 : all packet arrived
        if len(packets) == int(n_packet.decode()):
            msg = "200"
            sock.sendto(msg.encode(), addr)
            packets.sort(key=lambda x: x.packet_number)
            for packet in packets :     
                f.write(packet.body)
            print ("%s finish!" % file_name)
            break             
    f.close()

def isValid(file):
    if file in os.listdir(path):
        return;
    else:   
        msg = "File doesn't exist"
        return msg

# bind the socket to the port
server_address = ('localhost', 10000)
print ('\n\r Starting up on %s port %s' % server_address)
sock.bind(server_address)


try: 
    while True:
        print('\n\r Waiting to connect...')
        data, address = sock.recvfrom(4096) 
        resp = data.decode('utf8')
        
        if data:
            menu = '\r\n\nWelcome to the server\r\n\rAvailable options:\r\n\r\nList -> View available files\r\nGet -> Download file\r\nPut -> Upload file\r\nExit -> exit\r\n'         
            sent = sock.sendto(menu.encode(), address)
    
            while True:
                choice, address = sock.recvfrom(1024)
                resp = choice.decode('utf8')
                            
                # views file
                if resp.lower() == 'list':
                    print('\nViews files:')
                    data = str( os.listdir(path) )   
                    print(data)
                    sock.sendto(data.encode(), address);
                    
                # download file
                elif resp[0:3].lower() == 'get':
                    filename = resp[4:len(resp)]   
                    ctr = isValid(filename)
                    if ctr == "File doesn't exist":
                        data = "File doesn't exist"
                        sock.sendto(data.encode(), address);
                        continue
                    print('\nDownload file: %s ' % filename)   
                    data = "ok"
                    sock.sendto(data.encode(), address)
                    download(filename, address)    
                    
                # upload file
                elif resp[0:3].lower() == 'put':
                    filename = resp[4:len(resp)]
                    print('\nUpload file:')
                    data = "ok"
                    sock.sendto(data.encode(), address)
                    upload(filename)
    
                else:
                    #return the menu to the client
                    data = menu
                    sock.sendto(data.encode(), address);
                    
            # close connection
            sock.close()
            break;
except Exception as err:
    print(err)        
        
