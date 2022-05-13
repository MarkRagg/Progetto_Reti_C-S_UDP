'''
                            UDP SERVER SOCKET
Dilaver Shtini
'''

import socket as sk
#per gestire i file
import os
import time

# Creo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r Starting up on %s port %s' % server_address)
sock.bind(server_address)

#specifico il percorso dove prendo i file da visualizzare
path = os.getcwd()+"\\file"

while True:
    print('\n\r Waiting to connect...')
    data, address = sock.recvfrom(4096) 
    
    if data:
        menu = '\r\nBenvenuto sul server\r\n\r\nOpzioni Disponibili\r\n\r\n1. Visualizzazione dei file dispoinibli\r\n2. Download file\r\n3. Upload file\r\n4. Esci\r\n'         
        time.sleep(2)
        sent = sock.sendto(menu.encode(), address)
        #print ('Sent menu back to %s' % (address))

        while True:
            choice, address = sock.recvfrom(1024)
            
            print('dentro while, choice -> "%s"' % choice.decode())
            
            # visualizza i file presenti sul server
            if choice.decode() == '1':
                print('Visualizzazione file:\n')
                data = str( os.listdir(path) )
                time.sleep(4)
                #for file in data:
                    #print(file)
                
                # download di un file sul server
            elif choice.decode() == '2':
                print('Download file:\n')
                
                # upload di un file sul server
            elif choice.decode() == '3':
                print('Upload file:\n')
            
                # eseguo la funzione di Exit
            elif choice.decode() == '4':
                print('Exit\n')
                data = "Exit"
                sock.sendto(data.encode(), address);
                break;
            else:
                data = menu
                    # restituisce le opzioni del menù al client
            sock.sendto(data.encode(), address);
        # chiude la connessione
        sock.close()
        break;
