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
from model_stock_predict import ModelPredict
st.title('Finance Predictions')
## data loading
ticker_str = st.text_input(label='Comma Separated Ticker Symbols', value='GSIT')#, ICAD, XAIR, LTRN, ARKK, ARKF, ARKW')
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
company_name = st.selectbox(label='stock to predict', options=ticker_list, index=0)
lookback_length= st.slider(label='look-back length: how many days back to train the model to look per prediction', min_value=10, max_value=100, value=40)
mf = ModelFit
nodes = st.slider(label='how many nodes for the neural network per layer', min_value=10, max_value=100, value=50)
model_dict = {'gru_model': mf.gru_model(nodes=nodes), 'lstm_dense_model': mf.lstm_dense_model(nodes=nodes)}
model_name = st.selectbox(label = 'which model to predict with', options = list(model_dict.keys()), index=0)
model = model_dict[model_name]
future_num_days = st.slider(label='future number of days to predict', min_value=1, max_value=100, value=15)
latest_day = st.slider(label='day to start predictions with from latest', min_value = -100, max_value=-1, value=-lookback_length)

## run
batch_size = 30
train_ds, val_ds, test_ds = KerasPreprocess.keras_batch_preprocess(stocks_df=stocks_df, company_name=company_name, metric=column_metric, lookback_length=lookback_length, batch_size=batch_size)
history, model = mf.train_model(train_data=train_ds, validation_data=val_ds, model=model)
test_error = ModelPredict.evaluate_model(model, test_ds)
train_error = pd.DataFrame(history.history)
prediction_data = KerasPreprocess.get_prediction_data(stocks_df=stocks_df, company_name=company_name, metric=column_metric, lookback_length=lookback_length, latest_day=latest_day)
predictions = ModelPredict.pred_next_days(future_num_days=future_num_days, previous_days=prediction_data, model=model)
future_fig = VisualizeStocks.plot_future(predictions=predictions, stocks_df=stocks_df, latest_day=latest_day, future_num_days=future_num_days, company_name=company_name, column_metric=column_metric)



st.text('test_error:{}'.format(test_error))
st.subheader('Train error and validation error by epoch of training')
st.dataframe(train_error)
st.pyplot(future_fig)


