import pandas as pd
import time
import os

COLS = ["FFSR1", "FFSR2", "FFSR3", "FFSR4", "RFSR1", "RFSR2", "RFSR3", "RFSR4", "WS", "Label"]

# The ESP32 sends data vector each 200ms
# So the rate of the data collection will be:
# DF_UPDATE_RATE * 200ms
# e.g. DF_UPDATE_RATE = 5, we will get new sample to the dataset each 1 sec.
DF_UPDATE_RATE = 5
DF_TOTAL_SAMPLES = 25

Labels = {
    "LC": 0,  # Laying Center
    "LL": 1,  # Laying Left
    "LR": 2,  # Laying Right
    "AL": 3,  # Alarm Left
    "AR": 4,  # Alarm Right
}

class CollectMode():
    def __init__(self, verbose: bool = True, label: int = 0):
        self.data_file = f"data_{time.strftime(f'%H-%M-%S_%d-%m-%Y', time.gmtime())}_{label}.csv"
        self.df = pd.DataFrame(columns=COLS)
        self.verbose = verbose
        self.count = 0
        self.stored = 0
        self.label = label

    def collect(self, data: str):
        self.count += 1

        if self.verbose:
            print(data + f" {self.label}")

        data = data.split(" ")[2: -1]
        data.append(self.label)
        self.df = self.df.append(pd.Series(data, index=COLS), ignore_index=True)

        try:
            if self.count % DF_UPDATE_RATE == 0:
                self.df.to_csv(self.data_file)
                self.stored += 1

        except ValueError:
            pass

        if self.stored == DF_TOTAL_SAMPLES:
            print(f"{DF_TOTAL_SAMPLES} samples written to {self.data_file}, quitting...")
            os._exit(0)



class PredMode():
    def __init__(self, verbose: bool = True):
        self.data_file = f"data_{time.strftime('%H-%M-%S_%d-%m-%Y', time.gmtime())}.csv"
        self.df = pd.DataFrame(columns=COLS)
        self.verbose = verbose
        self.count = 0

    def collect(self, data: str):
        raise NotImplementedError

if __name__ == '__main__':
    print("Fall Prevention Modes Library")