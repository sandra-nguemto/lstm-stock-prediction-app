import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from configs import stocks, config

# Getting the required data from the yahoo finance API.
# We get the dates and adjusted close prices of the following stocks, for the period from 2004-10-30 to 2024-10-30.

# stocks = {'Walmart': 'WMT'}

dfs = {}


end_date = date.today()
start_date = end_date - relativedelta(years = 25)

end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

for key in stocks.keys():
    
    # dfs[key] = yf.Ticker(stocks[key]).history(start = start_date, end = end_date, auto_adjust = False, actions = False)['Adj Close']
    dfs[key] = yf.Ticker(stocks[key]).history(start = start_date, end = end_date, auto_adjust = False, actions = False)['Close']

class GetData:
    def __init__(self):
        self.data = dfs
    
    def get_dates(self):
        return self.data['Walmart'].index.strftime('%Y-%m-%d')
    
    def get_data(self):
        adj_closes = {}
        for key in self.data.keys():
            adj_closes[key] = np.array(self.data[key].values)
        return self.get_dates(), adj_closes            


        