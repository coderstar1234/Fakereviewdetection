# streamlit_app.py
import streamlit as st
import requests
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

# Load NLTK resources
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Load pickle files (replace with your actual paths)
model = None  # Replace with your model loading code
vectorizer = None  # Replace with your vectorizer loading code

# Import functions from notebooks



# Function to make a request to the Flask app
def send_review_to_flask(review):
    url = "http://localhost:5000/receive_review"  # Update with your Flask app's URL
    payload = {"review": review}
    response = requests.post(url, json=payload)
    return response.text

# Function for text preprocessing
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters, numbers, and extra whitespaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Apply stemming
    ps = PorterStemmer()
    words = [ps.stem(word) for word in words]

    # Join the words back into a string
    cleaned_text = ' '.join(words)

    return cleaned_text

# Assuming you have a function for determining the final prediction
def determine_final_prediction(pred1, pred2, pred3):
    # Your logic to combine or vote for the final prediction
    # For demonstration purposes, using a simple voting mechanism
    return max(set([pred1, pred2, pred3]), key=[pred1, pred2, pred3].count)

# Function for text classification in Streamlit
def text_classification_in_streamlit(review):
    # Replace the following with your actual model prediction logic
    # Example: prediction = model.predict(vectorizer.transform([preprocess_text(review)]).toarray())
    prediction1 = True  # Replace with your actual prediction
    prediction2 = False  # Replace with your actual prediction
    prediction3 = True  # Replace with your actual prediction

    # Call the function to determine the final prediction
    final_prediction = determine_final_prediction(prediction1, prediction2, prediction3)

    return final_prediction

# -- IMPLEMENTATION OF THE CLASSIFIER --
st.subheader("Fake Review Classifier")
review = st.text_area("Enter Review: ")
if st.button("Check"):
    # Use the correct function name: text_classification_in_streamlit
    result = text_classification_in_streamlit(review)
    st.write("Final Prediction:", result)

    # Send the review to Flask app
    flask_response = send_review_to_flask(review)
    st.write("Flask Response:", flask_response)
