import socket as sk
import os
import client_utils

# Create socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
sock.settimeout(2)

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

        sent = sock.sendto(message.encode(), server_address)
        print("")
        print("Message inviated")

        # Wait again a server message
        print("Waiting a response\n")
        data, server = sock.recvfrom(4096)
        response = data.decode('utf8')
        print ('Server message: %s' % response)

        if message == 'exit':
            print('exit from server..')
            break
        
        # Implementation of command put filename
        elif message[0:3] == 'put':
            # If server response with ok client is allowed to send the file
            if response == "ok":
                filename = upload_path + message[4:len(message)]
                client_utils.__upload__(sock, filename, server_address)
            else:
                break
        
        elif message[0:3] == 'get':
           # If server response with ok client is allowed to get the file
            if response == "ok":
                filename = download_path + message[4:len(message)]
                print("Start Downloading..")
                client_utils.__download__(sock, filename, server_address)
            else:
                break
            

        

except Exception as info:
    print(info)
    sock.sendto(message.encode(), server_address)
