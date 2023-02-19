from .fall_prevention_mode import *

HEIGHT_MIN = 120
HEIGHT_MAX = 220
WEIGHT_MIN = 40
WEIGHT_MAX = 150

class CollectMode(Mode):
    def __init__(self, verbose: bool = True, label: int = 0, weight = 0, height = 0):
        super().__init__(verbose)
        self.data_file = f"datasets/data_{time.strftime(f'%H-%M-%S_%d-%m-%Y', time.gmtime())}_{label}.csv"
        self.df = pd.DataFrame(columns=COLS)
        self.label = label
        self.weight = weight
        self.height = height

    def collect(self, data: str):
        if self.verbose:
            print(data + f" {self.label}")

        data = data.split(" ")[2: -1]
        data.append(int(self.weight))
        data.append(int(self.height))
        data.append(int(self.label))

        if len(data) != len(COLS):
            return False

        try:
            self.df = self.df.append(pd.Series(data, index=COLS), ignore_index=True)
            self.count += 1

        except ValueError:
            return False

        if self.count == DF_TOTAL_SAMPLES:
            self.df.to_csv(self.data_file)
            print(f"{DF_TOTAL_SAMPLES} samples written to {self.data_file}, quitting...")
            return True

        return False


if __name__ == '__main__':
    print("Fall Prevention Collect Mode")