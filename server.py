#!/bin/python3
import socket
import threading

# Connection Data
host = 'localhost'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message, ex=""):
    for client in clients:
        if client != ex:
            client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            index = clients.index(client)
            nickname = nicknames[index]
            message = client.recv(1024).decode('ascii')
            broad = '{}: {}'.format(nickname,message).encode('ascii')
            broadcast(broad,client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if nickname == '':
            nickname = "unknown" + str(len(nicknames)+1)
        else:
            print("no nick: " + nickname)
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'),client)
        #client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
