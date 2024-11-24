from data_preprocess import ModelData
from model import LSTMModel
from torch.utils.data import DataLoader
import torch.optim as optim
import torch
import torch.nn as nn
from configs import config, stocks






class Models():
    def __init__(self,config,stocks):
        self.config = config
        self.stocks = stocks
        

    def models(self):
        models = {}
        for key in self.stocks.keys():
            models[key] = LSTMModel(
                input_size=self.config["model"]["input_size"],
                hidden_layer_size=self.config["model"]["lstm_size"],
                num_layers=self.config["model"]["num_lstm_layers"],
                output_size=1,
                dropout=self.config["model"]["dropout"]
            )
            models[key] = models[key].to(self.config["training"]["device"])
            
        return models

#~################################################################   

class Dataloaders():
    def __init__(self,config,stocks):
        self.config = config
        self.stocks = stocks
        self.data = ModelData()
        self.train_data, self.test_data = self.data.model_data()
        
    def dataloaders(self):

        train_loader = {}
        test_loader = {}
        for key in self.stocks.keys():
            train_loader[key] = DataLoader(self.train_data[key], batch_size=self.config["training"]["batch_size"], shuffle=True)
            test_loader[key] = DataLoader(self.test_data[key], batch_size=self.config["training"]["batch_size"], shuffle=True)
        return train_loader, test_loader

#~################################################################   
class Trainer:
    def __init__(self, config, stocks, model):
        self.config = config
        self.stocks = stocks
        self.model = model
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config["training"]["learning_rate"], betas=(0.9, 0.98), eps=1e-9)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=self.config["training"]["scheduler_step_size"], gamma=0.1)


    def run_epoch(self, dataloader, is_training=False):
            
            epoch_loss = 0
    
            if is_training:
                self.model.train()
            else:
                self.model.eval()
    
            for idx, (x, y) in enumerate(dataloader):
                if is_training:
                    self.optimizer.zero_grad()
    
                batchsize = x.shape[0]
    
                x = x.to(self.config["training"]["device"])
                y = y.to(self.config["training"]["device"])
    
                out = self.model(x)
                loss = self.criterion(out.contiguous(), y.contiguous())
    
                if is_training:
                    loss.backward()
                    self.optimizer.step()
    
                epoch_loss += (loss.detach().item() / batchsize)
    
            lr = self.scheduler.get_last_lr()[0]
    
            return epoch_loss, lr

    def train(self, train_loader, test_loader):

        for epoch in range(self.config["training"]["num_epoch"]):
            loss_train, lr_train = self.run_epoch(train_loader, is_training=True)
            loss_test, _ = self.run_epoch(test_loader, is_training=False)
            self.scheduler.step()

            print('Epoch[{}/{}] | loss train:{:.6f}, test:{:.6f} | lr:{:.6f}'
              .format(epoch+1, self.config["training"]["num_epoch"], loss_train, loss_test, lr_train))
        




#~################################################################   
class TrainerAll():
    def __init__(self, config, stocks):
        self.config = config
        self.stocks = stocks
        self.models = Models(config, stocks).models()
        self.train_loader, self.test_loader = Dataloaders(config, stocks).dataloaders()
        

    def train_all(self):
        for key in self.stocks.keys():
            print(f"Training {key}-------------------")
            trainer = Trainer(self.config, self.stocks, self.models[key])
            trainer.train(self.train_loader[key], self.test_loader[key])
            torch.save(self.models[key], f"{key}.pth")    
        


        





