#!/usr/bin/env python
# coding: utf-8
import sys
print(sys.executable)
from ingest_stocks_to_df import ingest_stocks_to_df
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from itertools import cycle
import seaborn as sns
from keras_preprocessing import KerasPreprocess

st.title('Finance Predictions')

ticker_str = st.text_input(label='Comma Separated Ticker Symbols', value='GSIT, ICAD, XAIR, LTRN, ARKK, ARKF, ARKW')
ticker_list = [ticker.strip() for ticker in ticker_str.upper().split(',')]

time_diff_years= st.slider(label='Years of Data to Load', min_value=1, max_value=10, value=1, step=1)
stocks_df = ingest_stocks_to_df(ticker_list=ticker_list, time_diff_years=time_diff_years)
st.dataframe(data=stocks_df)

stock_names = st.multiselect(options=ticker_list, label='Stock To Plot', default=ticker_list[0])

column_metric = 'Adj Close'
def add_stocks_fig(stock_names, column_metric,stocks_df):
    indecies =  [*zip(stock_names, cycle([column_metric]))]
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_ylabel(column_metric)
    ax.grid()
    for index in indecies:
        ax = sns.lineplot(data=stocks_df, x='date', y=index, ax=ax)
    return fig
fig = add_stocks_fig(stock_names, column_metric,stocks_df)
st.pyplot(fig)

## predictions





