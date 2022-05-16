import socket as sk
import time
import os
import client_utils

# Create socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = "I'm a user"
response = ""
# Get path for directory 
upload_path = os.getcwd()+"\\ToUpload\\"
download_path = os.getcwd()+"\\Download\\"


try:
    # send message to server
    print ('sending %s' % message)
    sent = sock.sendto(message.encode(), server_address)

    # Wait server receive
    print('waiting to receive from')
    data, server = sock.recvfrom(4096)
    response = data.decode('utf8')
    # Print server info
    print ('Server message: %s' % response)

    while True:
        # Get command in input and send it to the server
        message = input("Write a command: ")

        if message == 'exit':
            print('exit from server..')
            break
        
        # Implementation of command put filename
        elif message[0:3] == 'put':
            # Send a message to the server with command put
            sock.sendto(message.encode(), server_address)

            # Waiting server response
            data, server = sock.recvfrom(4096)
            response = data.decode('utf8')

            # If server response with ok client is allowed to send the file
            if response == "ok":
                filename = upload_path + message[4:len(message)]
                client_utils.__upload__(sock, filename, server_address)
            else:
                break
            
            break
        
        elif message[0:3] == 'get':
            # Send a message to the server with command put
            sock.sendto(message.encode(), server_address)

            # Waiting server response
            data, server = sock.recvfrom(4096)
            response = data.decode('utf8')
            # If server response with ok client is allowed to send the file
            if response == "ok":
                filename = download_path + message[4:len(message)]
                print("Start Donwloading..")
                client_utils.__download__(sock, filename, server_address)
            else:
                break
            
            break

        sent = sock.sendto(message.encode(), server_address)
        print("")
        print("Message inviated")

        # Wait again a server message
        print("Waiting a response\n")
        data, server = sock.recvfrom(4096)
        response = data.decode('utf8')
        print ('Server message: %s' % response)

except Exception as info:
    print(info)
