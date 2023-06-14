import socket
import sys
import threading

BUFFER = 1024

class Server:
    def __init__(self, port):
        self.port = port
        self.serv_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_obj.setblocking(True)
        self.serv_obj.bind(('',self.port))
        self.serv_obj.listen()
        self.clients = {}
        connections = threading.Thread(target=self.handleConnections)
        connections.start()
        connections.join()

    def handleConnections(self):
        print(f"Starting server on port {self.port}")
        print("Tell your frends this!")
        while True:
            try:
                print('accepting connections again')
                client_obj, client_address = self.serv_obj.accept()
                client_obj.send(f"Enter a new nickname: ".encode('utf-8'))
                threading.Thread(target=self.handleClient, args=(client_obj,)).start()
            except KeyboardInterrupt:
                self.serv_obj.close()
                break

    def handleClient(self, client):
        nickname = client.recv(BUFFER).decode('utf-8').split(' ')[1]
        while nickname in self.clients.values() and not nickname.startswith('Nickname'):
            client.send(f"Enter a new nickname: ".encode('utf-8'))
            nickname = client.recv(BUFFER).decode('utf-8')
        self.clients[client] = nickname
        client.send(f"Nickname: {nickname}".encode('utf-8'))
        while True:
            message = client.recv(BUFFER)
            if message.decode('utf-8') == "quit":
                client.close()
                del self.clients[client]
                break
            for user in self.clients:
                user.send(message)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    serv = Server(port)