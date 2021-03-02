#!/usr/bin/env python
# coding: utf-8

# ## Data Ingestion.
## if packages aren't installed yet, run the following line
# !pip install matplotlib seaborn pandas numpy pandas_datareader requests_cache
import pandas as pd
import numpy as np
from pandas_datareader.data import DataReader
from datetime import datetime, timedelta, date

def ingest_stocks_to_df(time_diff_years=6, stock_list=['GSIT', 'ICAD', 'XAIR', 'LTRN', 'ARKK', 'ARKF', 'ARKW']):
    ## The tech stocks we'll use for this analysis
    ## Set up End and Start times for data grab
    end = datetime.now()
    start = datetime(end.year - time_diff_years, end.month, end.day)
    ## For loop for grabing yahoo finance data and setting as a dataframe
    stocks_dict = dict()
    for stock in stock_list:   
        ## Set DataFrame as the Stock Ticker
        stocks_dict[stock] = DataReader(stock, 'yahoo', start, end)
    ## Quick note: Using globals() is a sloppy way of setting the DataFrame names, but its simple
    ## these are from the globals() variables
    company_list = [stocks_dict[stock] for stock in stock_list]
    for company, stock_name in zip(company_list, stock_list):
        company["company_name"] = stock_name
    ## adds all the dataframes into one larger
    stocks_df = pd.concat(company_list, axis=0)
    ## shows a random selection of rows
    return stocks_df