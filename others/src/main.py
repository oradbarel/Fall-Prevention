from fall_prevention_server import Server
from fall_prevention_modes import CollectMode, PredMode


NUM_CLIENTS = 1
PORT = 13380
IP = "192.168.38.232"
ADDR = (IP, PORT)


def main():
    collect_mode = CollectMode(verbose=True)
    server = Server(addr=ADDR, num_clients=NUM_CLIENTS, operator=collect_mode)
    
    server.start()

if __name__ == '__main__':
    main()