from .fall_prevention_mode import *
from fall_prevention_ml import *

import pandas as pd
import numpy as np
import tensorflow as tf

SEQ_LEN = 4
DATA_LEN = 8
STOCK_SAMPLE = [0.0] * DATA_LEN
PRED_COLS = ["FFSR1", "FFSR2", "FFSR3", "FFSR4", "RFSR1", "RFSR2", "RFSR3", "RFSR4"]

def preprare_data(training_data, new_data):
    data_prep = data_preparation(training_data, new_data)
    return data_prep.prepare()

class PredMode(Mode):
    def __init__(self, verbose: bool = True):
        super().__init__(verbose)
        self.train = pd.read_csv("fall_prevention_ml/train.csv")
        self.train.drop(columns=self.train.columns[0], axis=1,  inplace=True)

        self.last_pred = 0
        self.window = [STOCK_SAMPLE for i in range(SEQ_LEN)]

        self.model = tf.keras.Sequential([tf.keras.models.load_model("fall_prevention_ml/fp_model.h5"), tf.keras.layers.Softmax()])
        self.counter = 0

    def collect(self, data: str):
        # Prepare current sample
        data = data.split(" ")[2: -1]
        
        if len(data) != len(PRED_COLS):
            return False

        self.counter += 1
        if self.verbose:
            print(data)

        sample = preprare_data(self.train, data)

        # Update sliding window
        self.window.append(sample.values.flatten().tolist())
        self.window.pop(0)

        # Get prediction
        curr = self.model.predict(np.array([pd.DataFrame(self.window, columns=PRED_COLS)]))
        self.last_pred =  [np.argmax(i) for i in curr][0]

        if self.verbose:
            print(self.last_pred, "Accuracy: ", curr[0][self.last_pred])

        return False

if __name__ == '__main__':
    print("Fall Prevention Predict Modes")
