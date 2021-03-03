#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import numpy as np
import pandas as pd
from ingest_stocks_to_df import IngestStocks
from visualize_stocks import VisualizeStocks
from keras_stock_preprocessing import KerasPreprocess
from model_stock_fit import ModelFit
from keras.utils import plot_model, model_to_dot

st.title('Finance Predictions')
## data loading
ticker_str = st.text_input(label='Comma Separated Ticker Symbols', value='GSIT, ICAD, XAIR, LTRN, ARKK, ARKF, ARKW')
ticker_list = [ticker.strip() for ticker in ticker_str.upper().split(',')]

time_diff_years= st.slider(label='Years of Data to Load', min_value=1, max_value=10, value=1, step=1)
stocks_df = IngestStocks.ingest_stocks_to_df(ticker_list=ticker_list, time_diff_years=time_diff_years)
st.dataframe(data=stocks_df)

## visualizations
stock_names = st.multiselect(options=ticker_list, label='Stock To Plot', default=ticker_list[0])

column_metric = 'Adj Close'
fig = VisualizeStocks.add_stocks_fig(stock_names=stock_names, column_metric=column_metric,stocks_df=stocks_df)
st.pyplot(fig)


## predictions
st.header('Predictions')
company_name = 'GSIT'
lookback_length=40


train_ds, val_ds, test_ds = KerasPreprocess.keras_batch_preprocess(stocks_df=stocks_df, company_name=company_name, metric=column_metric, lookback_length=lookback_length)
mf = ModelFit
model=mf.gru_model

history, model = mf.train_model(train_data=train_ds, validation_data=val_ds, model=model)
# st.graphviz_chart(model_to_dot(model, rankdir="LR"))
test_error = mf.evaluate_model(model=model, test_data=test_ds)
st.text('test_error:{}'.format(test_error))
st.subheader('Train error and validation error by epoch of training')
train_error = pd.DataFrame(history.history)
st.dataframe(train_error)


