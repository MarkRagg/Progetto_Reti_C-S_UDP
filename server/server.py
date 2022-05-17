'''
                            UDP SERVER SOCKET
Dilaver Shtini
'''

import socket as sk
import os
import time
import pickle
from packet import Packet
import hashlib

#path to get files
path = os.getcwd()+"\\file"

resp = ""

# create the socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Download files from server to client
def download(file_name, address):

    # set timeout for receive packet from client
    sock.settimeout(20)

    # open the file that client want
    file_path = path+"\\"+file_name
    f = open(file_path, "rb")
    data = f.read(1024)
    
    # start send packet
    while(data):
        if(sock.sendto(data, address)):
            data = f.read(4096)
            time.sleep(0.02) # give receiver a bit time to save
    f.close()
    
# Upload files from client to server
def upload(file_name):    
    
    # set timeout for receive packet from client
    sock.settimeout(2)

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
        print(n_packet.decode())
        x = "Header arrived"
        sock.sendto(x.encode(), addr)
        
        # now i can receive the data from the client
        i = 0
        
        # list for all packets received from client
        packets = []
       
        while i < int(n_packet.decode()):
            try:
                data, addr = sock.recvfrom(4096)    
                print(data.encode())
                data_enc  = pickle.loads(data)
                checksum = hashlib.md5(data_enc).digest()
                if checksum != data_enc.checksum:
                    i = 0
                    msg = "111"      
                    packets.clear()
                    sock.sendto(msg, addr)
                    continue 
                i = i+1
                # add the data received from client to the list
                packets.append(data_enc)
            except Exception as error:
                print(error)
                i = 0
                msg = "111"      # 111 : something going wrong
                packets.clear()
                sock.sendto(msg.encode(), addr)
            
        # 200 : all packet arriver
        if len(packets) == n_packet:
            msg = "200"
            sock.sendto(msg, addr)
            f.write(packets)
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


while True:
    print('\n\r Waiting to connect...')
    data, address = sock.recvfrom(4096) 
    resp = data.decode('utf8')
    
    if data:
        menu = '\r\nWelcome to the server\r\n\rAvailable options:\r\n\r\nList -> View available files\r\nGet -> Download file\r\nPut -> Upload file\r\nExit -> exit\r\n'         
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
                sock.sendto(data.encode(), address);
                
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
        
        
