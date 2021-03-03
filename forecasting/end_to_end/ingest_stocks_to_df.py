#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from pandas_datareader.data import DataReader
from datetime import datetime
class IngestStocks:
	@classmethod
	def ingest_stocks_to_df(cls,time_diff_years=6, ticker_list=['GSIT', 'ICAD', 'XAIR', 'LTRN', 'ARKK', 'ARKF', 'ARKW']):
	    """Takes list of stock tickers to pull from yahoo; returns dataframe, multi-indexed"""
	    file_name = cls.get_file_name(time_diff_years=time_diff_years, ticker_list=ticker_list)
	    try:
	    	stocks_df = pd.read_pickle(file_name)
	    except:
		    end = datetime.now()
		    start = datetime(end.year - time_diff_years, end.month, end.day)
		    dfs = [DataReader(stock, 'yahoo', start, end) for stock in ticker_list]
		    stocks_df = pd.concat(dfs, axis=1, join='outer', keys=ticker_list)
		    stocks_df.insert(loc=0, column='date', value=stocks_df.index)
		    stocks_df.to_pickle(file_name)
	    return stocks_df
	@staticmethod
	def get_file_name(time_diff_years=None, ticker_list=None):
		tickers_string = '_'.join(ticker_list)
		file_name = './data/stocks_df_years_{}_tickers_{}.pkl'.format(time_diff_years, tickers_string)
		return file_name
