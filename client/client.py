import socket as sk
import time


# Create socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = "I'm a user"
response = ""

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
            
        sent = sock.sendto(message.encode(), server_address)
        print("Message inviated")

        # Wait again a server message
        print("Waiting a response")
        data, server = data, server = sock.recvfrom(4096)
        response = data.decode('utf8')
        print ('Server message: "%s"' % response)

except Exception as info:
    print(info)
