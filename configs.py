from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / 'api_key.env'

load_dotenv(dotenv_path=env_path)

config = {"alpha_vantage": {
        "key": os.getenv("ALPHA_VANTAGE_API_KEY"),
        "outputsize": "full",
        "key_adjusted_close": "4. close",
    },
    "data": {
        "window_size": 5,
        "train_split_size": 0.80,
    }, 
    "model": {
        "input_size": 1, # since we are only using 1 feature, close price
        "num_lstm_layers": 2,
        "lstm_size": 32,
        "dropout": 0.2,
    },
    "training": {
        "device": "cpu", # "cuda" or "cpu"
        "batch_size": 64,
        "num_epoch": 100,
        "learning_rate": 0.01,
        "scheduler_step_size": 40,
    },
    "plots": {
        "show_plots": True,
        "xticks_interval": 90,
        "color_actual": "#001f3f",
        "color_train": "#3D9970",
        "color_val": "#0074D9",
        "color_pred_train": "#3D9970",
        "color_pred_val": "#0074D9",
        "color_pred_test": "#FF4136",
    }
}

stocks = {'Walmart': 'WMT', 
          'Amazon': 'AMZN',
          'Apple': 'AAPL',
          'Kroger': 'KR'}


# stocks = {'Walmart': 'WMT', 
#           'Amazon': 'AMZN',
#           'Apple': 'AAPL',
#           'CVSHealth': 'CVS',
#           'ExxonMobil': 'XOM',
#           'Alphabet': 'GOOGL',
#           'Cencora': 'COR',
#           'JPMorgan Chase & Co.': 'JPM',
#           'Chevron Corporation': 'CVX',
#           'Bank of America Corporation': 'BAC'}