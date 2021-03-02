from tensorflow.keras.preprocessing import timeseries_dataset_from_array
import numpy as np
class KerasPreprocess:
    def __init__():
        pass
    @classmethod
    def keras_batch_preprocess(cls, stocks_df=None, company_name=None, metric=None, lookback_length=60, batch_size=30):
        column_list = cls.get_column_list(stocks_df, company_name, metric)
        data, targets = cls.get_data_targets_split(column_list, lookback_length=lookback_length)
        data_train, data_val, data_test = cls.train_val_test_split(data)
        targets_train, targets_val, targets_test = cls.train_val_test_split(targets)
        train_ds = timeseries_dataset_from_array(data=data_train, targets=targets_train, sequence_length=lookback_length, batch_size=batch_size)
        val_ds = timeseries_dataset_from_array(data=data_val, targets=targets_val, sequence_length=lookback_length, batch_size=batch_size)
        test_ds = timeseries_dataset_from_array(data=data_test, targets=targets_test, sequence_length=lookback_length, batch_size=batch_size)
        return train_ds, val_ds, test_ds
    @staticmethod
    def get_column_list(stocks_df, company_name, metric):
        column_slice = stocks_df[company_name, metric]
        column_list = column_slice.tolist()
        return column_list
    @staticmethod
    def get_data_targets_split(column_list, lookback_length=None):
        data = np.array([[x] for x in column_list[:-lookback_length]])
        targets = np.array([y for y in column_list[lookback_length:]])
        return data, targets
    @staticmethod
    def train_val_test_split(data, test_size=0.2):
        test_length = int(len(data)*test_size)
        train_length = 1 - 2*test_length
        train = data[:train_length]
        val = data[train_length:train_length+test_length]
        test = data[-test_length:]
        return train, val, test