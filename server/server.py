'''
                            UDP SERVER SOCKET
Dilaver Shtini
'''

import socket as sk
import os
import time

#path to get files
path = os.getcwd()+"\\file"

resp = ""

# Download files from server to client
def download(file_name, address):

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
    while True:
        data, addr = sock.recvfrom(4096)
        if data:
            print ("File name: %s" % file_name)
            file_msg = data.strip()

        # create the new file on the server without content
        new_path = path+"\\"+file_name
        f = open(new_path, 'wb')

        # prendo il primo elemento che mi dice quanti pacchetti mi deve spedire il client
        n_packet = file_msg[0]
        # populate the file
        f.write(file_msg)
        print ("%s finish!" % file_name)
        break
    f.close()

def isValid(file):
    if file in os.listdir(path):
        return;
    else:
        msg = "File doesn't exist"
        return msg

# create the socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

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
        
        
