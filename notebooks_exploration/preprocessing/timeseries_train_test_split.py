#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from datetime import date
class TimeseriesTestTrainSplit:
    def __init__(self):
        pass
    @classmethod
    def timeseries_test_train_split(cls, stock_name='GSIT'):
        stocks_df = cls.load_df()
        data = cls.get_data(stocks_df, stock_name)
        train_length = cls.get_train_length(data)
        training_set, test_set = cls.get_train_test_split(data, train_length)
        X_train, y_train = cls.get_x_y_split(training_set)
        X_test, y_test = cls.get_x_y_split(test_set)
        return X_train, y_train, X_test, y_test
    def load_df():
        stocks_df = pd.read_pickle('./data/stocks_df_{}.pickle'.format(date.today()))
        stocks_df.sort_values(by=['Date'], inplace=True)
        return stocks_df
    def get_data(stocks_df, stock_name):
        data = stocks_df[stocks_df.company_name==stock_name]['Adj Close']
        return data
    def get_train_length(data):
        train_length = int(np.ceil(len(data.values)*0.8))
        if len(data.values) - train_length < 63:
            train_length = len(data.values) - 63
        return train_length
    def get_train_test_split(data, train_length):
        training_set = data.iloc[:train_length].values
        test_set = data.iloc[train_length:].values
        return training_set, test_set
    def get_x_y_split(data_set):
        # Creating a data structure with 60 time-steps and 1 output
        length=len(data_set)
        X = []
        y = []
        for i in range(60, length):
            X.append(data_set[i-60:i])
            y.append(data_set[i])
        X, y = np.array(X), np.array(y)
        X.reshape(-1, 1)
#         X = np.reshape(X, (X.shape[0], X.shape[1]))
        return X, y