import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class VisualizeStocks:
	@staticmethod
	def add_stocks_fig(stock_names=None, column_metric=None,stocks_df=None):
	    indecies =  [*zip(stock_names, cycle([column_metric]))]
	    fig = plt.figure()
	    ax = fig.add_subplot()
	    ax.set_ylabel(column_metric)
	    ax.grid()
	    for index in indecies:
	        ax = sns.lineplot(data=stocks_df, x='date', y=index, label=index[0], ax=ax)
	    return fig
	@staticmethod
	def plot_future(predictions=None, stocks_df=None, latest_day=None, future_num_days=None, company_name=None, column_metric=None):
		lookback_df = stocks_df.iloc[latest_day:latest_day+future_num_days]
		actual = lookback_df[(company_name, column_metric)]
		fig = plt.figure()
		ax = fig.add_subplot()
		ax.grid()
		ax = sns.lineplot(data=actual, ax=ax)
		ax.plot(lookback_df.date, predictions)
		return fig