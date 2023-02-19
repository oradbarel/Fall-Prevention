from abc import ABC, abstractmethod
import pandas as pd
import time
import os
from enum import Enum, auto

COLS = ["FFSR1", "FFSR2", "FFSR3", "FFSR4", "RFSR1", "RFSR2", "RFSR3", "RFSR4", "Weight", "Height", "Label"]

# The ESP32 sends data vector each 200ms
# So the collection lengh will be:
# time_t = DF_TOTAL_SAMPLES * 200ms
# e.g. DF_TOTAL_SAMPLES = 64, t_time = 64 * 200ms = 12.8 secs
DF_TOTAL_SAMPLES = 64

class Position(Enum):
    LAYING = 0
    LEFT_ALARM = auto()
    RIGHT_ALARM = auto()


class Mode(ABC):
    @abstractmethod
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.count = 0

    @abstractmethod
    def collect(self, data: str):
        pass

if __name__ == '__main__':
    print("Fall Prevention Mode")