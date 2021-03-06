'''
Generates dataframe for multiple tickers

input -- ticker.csv 

output -- dataframe with each output column representing one ticker 

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def test_run():
	''' Scan through the symbols'''
	start_date='2010-01-22'
	end_date='2015-02-10'
	# generate date range
	dates=pd.date_range(start_date,end_date)	
	df=pd.DataFrame(index=dates)
	
	# gget spy data and organize it
	symbol='SPY'
	dfSPY=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])

	dfSPY=dfSPY.rename(columns={'Adj Close':'SPY'})	
	# joine the two sets
	df=df.join(dfSPY,how='inner') # with inner added, it allows you to remove nan

	symbols=['GOOG','AAPL','GLD','A']

	for symbol in symbols:
		dfTemp=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])

		dfTemp=dfTemp.rename(columns={'Adj Close':symbol})	
		# joine the two sets
		df=df.join(dfTemp,how='inner') # with inner added, it allows you to remove nan
	
	#print(df1)
	return df

def load_dataFrame(start_date,end_date,symbols):
	''' Scan through the symbols'''
	# generate date range
	dates=pd.date_range(start_date,end_date)	
	df=pd.DataFrame(index=dates)

	for symbol in symbols:
		dfTemp=pd.read_csv("data/{}.csv".format(symbol),index_col="Date",parse_dates=True,
		usecols=['Date','Adj Close'],
		na_values=['nan'])

		dfTemp=dfTemp.rename(columns={'Adj Close':symbol})	
		# joine the two sets
		df=df.join(dfTemp,how='inner') # with inner added, it allows you to remove nan
	
	#print(df1)
	return df


def plot_stocks(df,title='Stock Prices'):
	''' plot stocks '''
	ax=df.plot(title=title)
	ax.set_xlabel('Dates')
	ax.set_ylabel('Prices')
	plt.show()

def normalize_data(df):
	''' scale all prices to so we can have relative values '''	
	df=df/df.ix[0,:]
	return df

def get_stats(df):
	''' calculate the mean, median and std of stocks'''
	mean=df.mean()
	median=df.median()
	stdDev=df.std()
	return (mean,median,stdDev) 

def get_rolling_mean(df,symbol='SPY'):
	''' get rolling mean of a ticker '''
	rm=pd.rolling_mean(df[symbol],window=20)
	return rm

def get_rolling_std(df,symbol='SPY'):
	''' get rolling std a ticker '''
	std=pd.rolling_std(df[symbol],window=20)
	return std

def plot_rm(df,symbol,rm):
	''' plot rolling mean and stock price '''
	ax=df[symbol].plot(title='Rolling Mean',label='SPY')
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	rm.plot(label='SPY Rolling Mean',ax=ax)
	ax.legend(loc='upper left')
	plt.show()

def plot_Bolling(df,symbol,band1,band2):
	''' plot Bolling and stock price '''
	ax=df[symbol].plot(title='Bolling Bands',label=symbol)
	ax.set_xlabel('Date')
	ax.set_ylabel('Price')
	band1.plot(label='SPY Band1',ax=ax)
	band2.plot(label='SPY Band2',ax=ax)
	ax.legend(loc='upper left')
	plt.show()
	

def compute_daily_return(df):
	'''' computes the daily returns for each column/ticker in dataframe '''
	df_returns=df/df.shift(1)-1
	return df_returns

def plot_daily_returns(df_returns,symbol):
	''' plot daily returns '''
	ax=df_returns[symbol].plot(label=symbol)
	ax.set_xlabel('Date')
	ax.set_ylabel('Returns')
	ax.legend(loc='upper left')
	plt.show()

def plot_hist(df_returns,symbol,bins=20):
	''' plot hist of returns '''
	mean=df_returns[symbol].mean()
	std=df_returns[symbol].std()
	kurtosis=df_returns[symbol].kurtosis()
	ax=df_returns[symbol].hist(bins=bins)
	plt.axvline(mean,color='r',linestyle='dashed',linewidth=2)
	plt.axvline(mean+std,color='g',linestyle='dashed',linewidth=2)
	plt.axvline(mean-std,color='g',linestyle='dashed',linewidth=2)
	plt.axhline(20,color='g',linestyle='dashed',linewidth=2)
	ax.set_xlabel('Returns')
	ax.set_ylabel('Frequency')
	ax.legend(loc='upper left')
	plt.show()

def plot_two_hist(df_returns,symbol1,symbol2,bins=20):
	''' plot hist of returns '''
	ax=df_returns[symbol1].hist(bins=bins,label=symbol1)
	df_returns[symbol2].hist(bins=bins,label=symbol2)
	ax.set_xlabel('Returns')
	ax.set_ylabel('Frequency')
	ax.legend(loc='upper left')
	plt.show()

def plot_scatter(df_returns,symbol1,symbol2):
	''' plot hist of returns '''
	ax=df_returns.plot(kind='scatter',x=symbol1,y=symbol2)
	beta,alpha=np.polyfit(df_returns[symbol1],df_returns[symbol2],1)
	print(alpha,beta)
	plt.plot(df_returns[symbol1],alpha+beta*df_returns[symbol1],'r-')
	ax.set_xlabel(symbol1)
	ax.set_ylabel(symbol2)
	ax.legend(loc='upper left')
	plt.show()

def get_corr(df_returns):
	''' Get correlation between returns'''
	return df_returns.corr(method='pearson')

if __name__=="__main__":
	# initialize the dates and tickers
	start_date='2010-01-22'
	end_date='2012-9-12'	
	symbols=['SPY','GOOG','GE','AAPL','GLD','A','CAT']
	symbol='AAPL'
	df=load_dataFrame(start_date,end_date,symbols)
	df=normalize_data(df)
	#plot_stocks(df)
	(dfmean,dfmedian,dfstd)=get_stats(df)
	print(dfmean)
	print(dfstd)
	rm=get_rolling_mean(df,symbol)
	std=get_rolling_std(df,symbol)
	#plot_rm(df,'SPY',rm)
	band1=rm-2*std
	band2=rm+2*std
	#plot_Bolling(df,symbol,band1,band2)

	df_returns=compute_daily_return(df)
	#plot_daily_returns(df_returns,'AAPL')
	#plot_stocks(df[['AAPL','CAT']])
	#plot_hist(df_returns,symbol,100)
	#plot_two_hist(df_returns,'AAPL','GE',100)
	#plot_scatter(df_returns,'SPY','SPY')
	dfcor=pd.DataFrame(get_corr(df_returns)) # save correlation matrix as dataframe for future reference
	print(dfcor.loc['GE']['CAT'])