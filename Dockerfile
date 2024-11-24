# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /flask_app

# Copy the application code and custom modules to the container
COPY app.py /flask_app/
COPY configs.py /flask_app/
COPY train.py /flask_app/
COPY data_preprocess.py /flask_app/
# COPY s_getdata.py /flask_app/
COPY getdata.py /flask_app/
COPY utils.py /flask_app/
COPY model.py /flask_app/
COPY Walmart.pth /flask_app/
COPY Amazon.pth /flask_app/
COPY Apple.pth /flask_app/
COPY Kroger.pth /flask_app/
COPY unseen.pth /flask_app/
COPY scalers.pth /flask_app/

# Install necessary Python dependencies
COPY requirements.txt /flask_app/
RUN pip install --no-cache-dir -r requirements.txt 

# Expose the port Flask uses (if running locally on port 5000)
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]

# docker build -t lstm-stock-prediction-app .
# docker run -p 5001:5000 lstm-stock-prediction-app
# http://localhost:5001/
