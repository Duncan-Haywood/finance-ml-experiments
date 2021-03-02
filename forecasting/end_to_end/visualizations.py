import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Visualizations:
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