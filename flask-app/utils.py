import numpy as np
from configs import config





class Normalizer():
    def __init__(self):
        self.mu = None
        self.sd = None

    def fit_transform(self, x):
        self.mu = np.mean(x, axis=(0), keepdims=True)
        self.sd = np.std(x, axis=(0), keepdims=True)
        normalized_x = (x - self.mu)/self.sd
        return normalized_x

    def inverse_transform(self, x):
        return (x*self.sd) + self.mu
    


#~################################################################   
class DataPrep():
    def __init__(self, config=config):
        self.config = config
        self.split_index = None

    def prepare_data_x(self, x, window_size):
    # perform windowing
        n_row = x.shape[0] - window_size + 1
        output = np.lib.stride_tricks.as_strided(x, shape=(n_row,window_size), strides=(x.strides[0],x.strides[0]))
        return output[:-1], output[-1]   


    def prepare_data_y(self, x, window_size):

        # use the next day as label
        output = x[window_size:]
        return output     
    
    def prepare_data(self, normalized_data_close_price, config):
        data_x, data_x_unseen = self.prepare_data_x(normalized_data_close_price, window_size=config["data"]["window_size"])
        data_y = self.prepare_data_y(normalized_data_close_price, window_size=config["data"]["window_size"])

        # split dataset

        self.split_index = int(data_y.shape[0]*config["data"]["train_split_size"])
        data_x_train = data_x[:self.split_index]
        data_x_val = data_x[self.split_index:]
        data_y_train = data_y[:self.split_index]
        data_y_val = data_y[self.split_index:]

        return  data_x_unseen, data_x_train, data_x_val, data_y_train, data_y_val