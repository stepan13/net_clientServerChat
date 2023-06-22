import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")
online = True

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(('91.200.148.112', 55555))
client.connect(('localhost', 55555))

# Listening to Server and Sending Nickname
def receive():
    global online
    while online:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                print("sent nick")
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            online = False
            break
    

def write():
    global online
    while online:
        #message = '{}: {}'.format(nickname, input(''))
        #print(nickname)
        message = input("")
        #message = '{}'.format()
        #message = '{}'.format('left')
        if message != '':
            client.send(message.encode('ascii'))
        if message == "exit":
            online = False
            client.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()