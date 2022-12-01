import pandas as pd
import time


COLS = ["FS1", "FS2", "FS3", "FS4", "FS5", "FS6", "FS7", "FS8", "WS"]
DF_UPDATE_RATE = 25


class CollectMode():
    def __init__(self, verbose: bool = True):
        self.data_file = f"data_{time.strftime('%H-%M-%S_%d-%m-%Y', time.gmtime())}.csv"
        self.df = pd.DataFrame(columns=COLS)
        self.verbose = verbose
        self.count = 0

    def collect(self, data: str):
        self.count += 1

        if self.verbose:
            print(data)

        data = data.split(" ")[2: -1]
        self.df = self.df.append(pd.Series(data, index=COLS), ignore_index=True)

        if self.count % DF_UPDATE_RATE == 0:
            self.df.to_csv(self.data_file)


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