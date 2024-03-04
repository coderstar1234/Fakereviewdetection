from flask import Flask, render_template, request, url_for, session, redirect
from flask_pymongo import PyMongo
from flask import jsonify  # Make sure to import jsonify
from flask import render_template
import requests  # Add this import
from flask_cors import CORS
import numpy as np
import pandas as pd
import sklearn as sk
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'intellipaat'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/intellipaat'


mongo = PyMongo(app)

model=pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        # Handle the form submission and redirect or perform necessary actions
        return redirect(url_for('root'))  # Use the correct endpoint name here
    else:
        # Render the index template for GET requests
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('home'))

        return 'Invalid username/password combination'

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'username': request.form['username'],
                'email': request.form['email'],  # Ensure 'email' is present in the form
                'password': hashpass
            })
            session['username'] = request.form['username']
            return redirect(url_for('home'))

        return 'Username already exists!'

    return render_template('signup.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Handle the form submission and login logic here
        # Redirect to the dashboard or perform necessary actions
        return redirect(url_for('dashboard'))
    else:
        # Render the dashboard template for GET requests
        return render_template('dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ... (your existing code)
# ... (your existing imports)

@app.route('/predict', methods=['POST'])
def predict():
    # Load the model and data preprocessing steps
    df = pd.read_csv('deceptive-opinion.csv')
    df1 = df[['deceptive', 'text']]
    df1.loc[df1['deceptive'] == 'deceptive', 'deceptive'] = 0
    df1.loc[df1['deceptive'] == 'truthful', 'deceptive'] = 1
    X = df1['text']
    Y = np.asarray(df1['deceptive'], dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=109)
    cv = CountVectorizer()
    x = cv.fit_transform(X_train)
    y = cv.transform(X_test)
    
    if request.method == 'POST':
        # Get the input from the form
        message = request.form.get('enteredinfo')
        
        # Check if the input is not empty
        if message:
            data = [message]
            vect = cv.transform(data).toarray()
            pred = model.predict(vect)
            return render_template('result.html', prediction_text=pred)
        else:
            # Handle the case when the input is empty
            return render_template('result.html', prediction_text="Please enter information for prediction.")

    # Render the result template for GET requests
    return render_template('result.html', prediction_text="")
    
# ... (the rest of your existing code)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

