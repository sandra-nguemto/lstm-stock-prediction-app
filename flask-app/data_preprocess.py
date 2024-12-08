# from getdata import GetData
from getdata import GetData
from sklearn.preprocessing import MinMaxScaler
import numpy as np
# from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from configs import config, stocks
from utils import Normalizer, DataPrep
import torch

import os

save_dir = "/lstm-stock-prediction-app/flask-app/"
os.makedirs(save_dir, exist_ok=True)


#~################################################################    

class Scaler:
    def __init__(self):
        self
        

    def scalers(self):
        scalers = {}
        for key in stocks.keys():
            # scalers[key] = Normalizer()
            scalers[key] = MinMaxScaler()
        return scalers    
        

#~################################################################     
class DataPreprocess:
    def __init__(self, lag = 20):
        self.lag = lag
        self.get_data = GetData()
        self.dates, self.data = self.get_data.get_data()
        self.scalers = Scaler().scalers()
        self.splitting = DataPrep()
        self.config = config
        self.stocks = stocks

    def scale_data(self):
        for key in self.data.keys():
            self.data[key] = self.scalers[key].fit_transform(self.data[key].reshape(-1, 1)).flatten()
        # torch.save(self.scalers, f"scalers.pth")
        scaler_path = os.path.join(save_dir, f"scalers.pth")
        torch.save(self.scalers, scaler_path)     
        return self.data     
        

    def split_data(self):
        self.data = self.scale_data()
        X_unseen = {}
        X_train, X_test, y_train, y_test = {}, {}, {}, {}    
        
        for key in self.stocks.keys():
            X_unseen[key], X_train[key], X_test[key], y_train[key], y_test[key] = self.splitting.prepare_data(self.data[key], self.config) 
            X_train[key] = np.expand_dims(X_train[key], axis = 2)
            X_test[key] = np.expand_dims(X_test[key], axis = 2)
        # torch.save(X_unseen, f"unseen.pth")   
        unseen_path = os.path.join(save_dir, f"unseen.pth") 
        torch.save(X_unseen, unseen_path)
        return X_train, X_test, y_train, y_test      
    
#~################################################################    
    

class TimeSeriesDataset(Dataset):
    def __init__(self, x, y):
        self.x = x.astype(np.float32)
        self.y = y.astype(np.float32)
        
    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return (self.x[idx], self.y[idx])
    
class ModelData(DataPreprocess):
    def __init__(self, lag = 20):
        super().__init__(lag)
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data()
        self.train_data, self.test_data = {}, {}
        for key in self.X_train.keys():
            self.train_data[key] = TimeSeriesDataset(self.X_train[key], self.y_train[key])
            self.test_data[key] = TimeSeriesDataset(self.X_test[key], self.y_test[key])
            
    def model_data(self):
        return self.train_data, self.test_data
    
