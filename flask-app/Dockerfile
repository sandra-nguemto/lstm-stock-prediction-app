# Use an official Python runtime as the base image
FROM python:3.9-slim




# Set the working directory inside the container
WORKDIR /lstm-stock-prediction-app/flask-app

# Copy the application code and custom modules to the container
# COPY app.py /lstm-stock-prediction-app/
# COPY configs.py /lstm-stock-prediction-app/
# COPY train.py /lstm-stock-prediction-app/
# COPY data_preprocess.py /lstm-stock-prediction-app/
# COPY getdata.py /lstm-stock-prediction-app/
# COPY utils.py /lstm-stock-prediction-app/
# COPY model.py /lstm-stock-prediction-app/
# COPY Walmart.pth /lstm-stock-prediction-app/
# COPY Amazon.pth /lstm-stock-prediction-app/
# COPY Apple.pth /lstm-stock-prediction-app/
# COPY Kroger.pth /lstm-stock-prediction-app/
# COPY unseen.pth /lstm-stock-prediction-app/
# COPY scalers.pth /lstm-stock-prediction-app/

COPY app.py configs.py train.py data_preprocess.py getdata.py utils.py model.py Walmart.pth Amazon.pth Apple.pth Kroger.pth unseen.pth scalers.pth /lstm-stock-prediction-app/flask-app/


# Install necessary Python dependencies
COPY requirements.txt /lstm-stock-prediction-app/flask-app/
# RUN pip install --no-cache-dir -r requirements.txt 
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==2.3.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html




# Expose the port Flask uses (if running locally on port 5000)
# EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]

# docker build -t lstm-stock-prediction-app .
# docker run -p 5001:5000 lstm-stock-prediction-app
# docker run -p 8080:80 lstm-stock-prediction-app 
# http://localhost:5001/

