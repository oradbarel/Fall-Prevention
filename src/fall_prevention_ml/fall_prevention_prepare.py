from sklearn.preprocessing import StandardScaler
from fall_prevention_modes import *
import tensorflow as tf
import pandas as pd

PRED_COLS = ["FFSR1", "FFSR2", "FFSR3", "FFSR4", "RFSR1", "RFSR2", "RFSR3", "RFSR4"]

class data_preparation():

    def __init__(self, training_data, new_data):
        self.new_data = pd.DataFrame(columns=PRED_COLS)
        self.new_data = self.new_data.append(pd.Series(new_data, index=PRED_COLS), ignore_index=True)

        self.training_data_ref = training_data


    def __normalize(self):
        all_features = list(self.training_data_ref.columns)

        for feature in all_features:
            std_scaler = StandardScaler()
            std_scaler.fit(self.training_data_ref[[feature]])

            self.new_data[[feature]] = std_scaler.transform(self.new_data[[feature]])

        return self.new_data

    def prepare(self):
        self.__normalize()
        return self.new_data
