import requests
import streamlit as st


# Dashboard Title

st.title('Stock Price Prediction')

# Fetch data from flask-app

response = requests.get('http://flask-app:5000/predict')
data = response.json()


# Display the data

for key, value in data.items():
    st.write(f"Stock: {key}")
    st.write(f"Predicted Price: {value}")
    st.write("----")