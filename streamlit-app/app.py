import requests
import streamlit as st


# Dashboard Title

st.title('Stock Price Prediction')

# Fetch data from flask-app

response = requests.get('http://flask:5000/predict')
data = response.json()

stock_data = data.get("outputs", {})
# Display the data

# for key, value in stock_data.items():
#     st.write(f"**Stock**: {key}")
#     st.write(f"**Predicted Price**: {value}")
#     st.write("----")

for key, value in stock_data.items():
    col1, col2 = st.columns([2, 1])  # Create two columns with different widths
    col1.markdown(f"### <span style='color:purple;'>**{key}** </span>", unsafe_allow_html=True)
    col2.markdown(f"**Predicted Price**<span style='color:black;'>: {value}</span>", unsafe_allow_html=True)
    st.write("----")  # Add a separator line
