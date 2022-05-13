import socket as sk
import time
import os

# Upload function
def __upload__(filename, address):
    filesize = os.path.getsize(filename)
    print(filename)
    packet = open(filename, "rb")
    while True:
        # Read bytes from the file
        bytes_read = packet.read(filesize)
        # If bytes_read not read any bytes file transfer is finished
        if not bytes_read:
            packet.close()
            break
        # Send a packet
        sock.sendto(bytes_read, address)

# Create socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = "I'm a user"
response = ""
# Get path for directory 
upload_path = os.getcwd()+"\\ToUpload\\"
download_path = os.getcwd()+"\\Download"


try:
    # send message to server
    print ('sending "%s"' % message)
    time.sleep(2)
    sent = sock.sendto(message.encode(), server_address)

    # Wait server receive
    print('waiting to receive from')
    data, server = sock.recvfrom(4096)
    response = data.decode('utf8')
    # Print server info
    time.sleep(2)
    print ('received message "%s"' % response)

    while True:
        # Get command in input and send it to the server
        message = input("Write a command: ")

        if message == 'Exit':
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
                __upload__(filename, server_address)
            else:
                break
            break
            
        sent = sock.sendto(message.encode(), server_address)
        print("Message inviated")

        # Wait again a server message
        print("Waiting a response")
        data, server = sock.recvfrom(4096)
        response = data.decode('utf8')
        print ('Server message: "%s"' % response)

except Exception as info:
    print(info)
