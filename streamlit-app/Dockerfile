FROM python:3.9-slim

WORKDIR /lstm-stock-prediction-app/streamlit-app

COPY requirements.txt /lstm-stock-prediction-app/streamlit-app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /lstm-stock-prediction-app/streamlit-app/

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
