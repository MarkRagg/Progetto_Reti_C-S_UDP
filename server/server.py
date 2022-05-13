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


def download(file_name, address):

    # open the file that client want
    f = open(path+"\\"+file_name, "rb")
    data = f.read(4096)
    
    # start send packet
    while(data):
        if(sock.sendto(data.encode(), address)):
            data = f.read(4096)
            time.sleep(0.02) # give receiver a bit time to save

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
        menu = '\r\nBenvenuto sul server\r\n\r\nOpzioni Disponibili\r\n\r\nList. Visualizzazione dei file disponibli\r\nGet. Download file\r\nPut. Upload file\r\n4. Esci\r\n'         
        time.sleep(2)
        sent = sock.sendto(menu.encode(), address)

        while True:
            choice, address = sock.recvfrom(1024)
            resp = choice.decode('utf8')
                        
            # views file
            if resp == 'list':
                print('Views files:\n')
                data = str( os.listdir(path) )   
                time.sleep(2)
                print(data)
                
                # download file
            elif resp[0:3] == 'get':
                filename = resp[4:len(resp)]   
                print('Download file: %s \n' % filename)   
                ctr = isValid(filename)
                if ctr == "File doesn't exist":
                    data = "File doesn't exist"
                    sock.sendto(data.encode(), address);
                    continue
                download(filename, address)                
                
                # upload file
            elif choice.decode() == '3':
                print('Upload file:\n')

            else:
                data = menu
                # return menu to client
            sock.sendto(data.encode(), address);
        # close connection
        sock.close()
        break;

    
    
    
    
    
    
    
    
    



