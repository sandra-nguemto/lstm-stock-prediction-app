from alpha_vantage.timeseries import TimeSeries 
from configs import config, stocks
import numpy as np




class GetData:
    def __init__(self, config=config, stocks=stocks): 
        self.config = config
        self.stocks = stocks
       
        
    def download_data(self, symbol):

        # get the data from alpha vantage
        ts = TimeSeries(key=self.config["alpha_vantage"]["key"])
        # print(config["alpha_vantage"]["key"])
        data, meta_data = ts.get_daily(symbol, outputsize=self.config["alpha_vantage"]["outputsize"])

        data_date = [date for date in data.keys()]
        data_date.reverse()

        data_close_price = [float(data[date][self.config["alpha_vantage"]["key_adjusted_close"]]) for date in data.keys()]
        data_close_price.reverse()
        data_close_price = np.array(data_close_price)
        

        return data_date, data_close_price

    def get_data(self):
        close_prices = {}
        dates = {}

        for key in self.stocks.keys():
            dates[key], close_prices[key] = self.download_data(symbol=self.stocks[key])

        return dates[list(self.stocks.keys())[0]], close_prices    
    