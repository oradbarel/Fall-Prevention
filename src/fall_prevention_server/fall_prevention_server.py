import socket
import time
from fall_prevention_modes import Mode, PredMode, CollectMode, Position,\
    WEIGHT_MIN, WEIGHT_MAX, HEIGHT_MIN, HEIGHT_MAX

DF_UPDATE_RATE = 25
MSG_LEN_MIN = 9
CHUNK_SIZE = 64


class Server():
    def __init__(self, addr: tuple, num_clients: int, operator):
        self.num_clients = num_clients
        self.operator = operator
        self.socket = None
        self.addr = addr
        self.client = None
        self.last_recv = time.time()

    def init(self):
        print("Starting...")
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Check this change
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.bind(self.addr)
        self.socket.listen(self.num_clients)
        print("Waiting for client...")
        client, addr = self.socket.accept()
        print("Got connection: " + str(addr))
        self.client = client
        

    def start(self):
        while True:
            data = self.client.recv(CHUNK_SIZE)
            data = data.decode('utf-8')

            self.last_recv = time.time()

            if len(data) <= MSG_LEN_MIN:
                continue

            if self.operator.collect(data):
                return


class CollectServer(Server):
    @staticmethod
    def getLabel() -> int:
        while(True):
            print("Choose Label (by the index):\n")
            print("0. Laying Center")
            print("1. Laying Left")
            print("2. Laying Right")
            print("3. Alarm Left")
            print("4. Alarm Right")
            label = input("Label -> ")
            try:
                label = int(label)
                if label in [p.value for p in Position]:
                    return label
            except (TypeError, ValueError):
                pass
            print("ERROR: Invalid Lable. Please try again.")

    @staticmethod
    def getHeight() -> int:
        while(1):
            height = input("Height -> ")
            try:
                height = int(height)
                if HEIGHT_MIN <= height <= HEIGHT_MAX:
                    return height
            except (TypeError, ValueError):
                pass
            print("ERROR: Invalid Height. Please try again.")

    @staticmethod
    def getWeight() -> int:
        while(1):
            weight = input("Weight -> ")
            try:
                weight = int(weight)
                if WEIGHT_MIN <= weight <= WEIGHT_MAX:
                    return weight
            except (TypeError, ValueError):
                pass
            print("ERROR: Invalid Weight. Please try again.")

    @staticmethod
    def getMode() -> CollectMode:
        label = CollectServer.getLabel()
        height = CollectServer.getHeight()
        weight = CollectServer.getWeight()
        print(f"New patient. Label = {label}, height = {height}, weight = {weight}.")
        return CollectMode(verbose=True, label=label, height=height, weight=weight)

    def __init__(self, addr: tuple, num_clients: int):
        super().__init__(addr, num_clients, operator=None)
        self.operator = CollectServer.getMode()

    def printCurrentPatient(self) -> None:
        label = self.operator.label
        height = self.operator.height
        weight = self.operator.weight
        print(
            f"Same patient. Label = {label}, height = {height}, weight = {weight}.")

    def updateMode(self) -> None:
        print("Done session for that label.")
        while(1):
            print("Keep smaple with the same patient?\t Y/n")
            try:
                decision = input("-> ").lower()
                if decision in ['y', 'n']:
                    break
            except:
                pass
            print("ERROR: Invalid Input. Please insert 'Y' or 'n'.")

        if decision == 'n':
            self.operator = CollectServer.getMode()
        else:
            new_operator = CollectMode(
                verbose=True,
                label=CollectServer.getLabel(),
                height=self.operator.height,
                weight=self.operator.weight)
            self.operator = new_operator
            self.printCurrentPatient()


if __name__ == '__main__':
    print("Fall Prevention Server Library")
