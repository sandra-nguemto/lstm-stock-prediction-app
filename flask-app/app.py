import torch
from train import Trainer, TrainerAll, Models
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from data_preprocess import DataPreprocess
from configs import config, stocks



app = Flask(__name__)

device = config["training"]["device"]

# Scheduler configuration
class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config)
scheduler = APScheduler()
scheduler.init_app(app)



# Load PyTorch models
model_app = {}
for key in stocks.keys():
    model_app[key] = torch.load(f"{key}.pth", map_location=device)
    model_app[key].eval()
# Load Unseen Data and scalers
unseen = torch.load("unseen.pth")
scalers = torch.load("scalers.pth")

#~################################################################

# Retrain function
def retrain_models():
    global model_app  # Access the global model dictionary
    print("Retraining models...")
    trainer = TrainerAll(config, stocks)
    trainer.train_all()
    for key in stocks.keys():
        # Reload the updated model into the Flask app
        model_app[key] = torch.load(f"{key}.pth", map_location=device)
        model_app[key].eval()
    print("Retraining completed!")

# Schedule retraining task
@scheduler.task('cron', id='daily_retraining', hour=0, minute=0)  # Runs daily at midnight
def scheduled_task():
    retrain_models()


#~################################################################

@app.route('/')
def predict():
    outputs = {}
    for key in stocks.keys():
        with torch.no_grad():
            # Preprocess inputs
            inputs = torch.tensor(unseen[key]).float().to(config["training"]["device"]).unsqueeze(0).unsqueeze(2)
            # Get prediction
            model_output = model_app[key](inputs).cpu().detach().numpy()
            # Rescale to original values
            scaled_output = scalers[key].inverse_transform(model_output.reshape(-1, 1)).flatten()[0]
            # Convert to list of Python float types
            outputs[key] = scaled_output.tolist()
    return jsonify({'outputs': outputs})


if __name__ == '__main__':
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, debug=True)




#~################################################################   

