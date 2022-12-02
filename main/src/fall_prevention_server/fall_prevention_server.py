import socket


DF_UPDATE_RATE = 25
MSG_LEN_MIN = 10
CHUNK = 4096


class Server():
    def __init__(self, addr: tuple, num_clients: int, operator):
        self.num_clients = num_clients
        self.operator = operator
        self.socket = None
        self.addr = addr
    
    def start(self):
        print("Starting...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.addr)
        self.socket.listen(self.num_clients)

        print("Waiting for client...")
        client, addr = self.socket.accept()
        print("Got connection: " + str(addr))

        while True:
            data = client.recv(CHUNK)
            data = data.decode('utf-8')

            if len(data) < MSG_LEN_MIN:
                continue

            self.operator.collect(data)


if __name__ == '__main__':
    print("Fall Prevention Server Library")