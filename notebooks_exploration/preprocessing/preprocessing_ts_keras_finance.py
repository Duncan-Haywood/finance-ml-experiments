#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
from keras.preprocessing.sequence import TimeseriesGenerator
def get_data_targets(stock_arr, sequence_inlength):
    """where stock_arr is sequential np.array and 
    sequence_inlength is the length of the data sequences"""
    x, y = list(), list()
    for index in range(sequence_inlength, len(stock_arr)):
        window = stock_arr[index-sequence_inlength:index]
        x.append(window)
        y.append([stock_arr[index]])
    data = np.array(x)
    targets = np.array(y)
    return data, targets
def test_train_split(data, targets, split=0.8):
    """both of np.array"""
    data_train_len = int(len(data)*split)
    targets_train_len = int(len(targets)*split)
    data_tr, targets_tr = data[:data_train_len], targets[:targets_train_len]
    data_test, targets_test = data[data_train_len:], targets[targets_train_len:]
    return data_tr, targets_tr, data_test, targets_test
def to_ts_data(stock, stocks_df, sequence_inlength=60):
    stock_arr = stocks_df[stocks_df.company_name == stock]['Adj Close'].to_numpy()
    data, targets = get_data_targets(stock_arr, sequence_inlength)
#     display(data, targets)
    data_tr, targets_tr, data_test, targets_test = test_train_split(data, targets, split=0.8)
    data_gen_train = TimeseriesGenerator(data_tr, targets_tr, length=sequence_inlength)
    data_gen_test = TimeseriesGenerator(data_test, targets_test, length=sequence_inlength)
    ##shape (number of batches, input number of steps before prediction, feature-dimensions for input)
    return data_gen_train, data_gen_test


# In[ ]:




