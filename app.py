# pip install -r requierments.txt

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key=os.urandom(24) # setting a secret key for session management

app.permanent_session_lifetime = timedelta(days=1)

@app.route('/')
def index():
    # Renders the home page.
    return render_template('index.html')

@app.route('/buy_sell.html', methods=['GET', 'POST'])
def buy_sell():
    #Handling buying and selling products.
    if request.method == 'POST':
        if 'user'in session:
            # Handling the request for logged-in users
            return 'Request Submitted!'
        else:
            return redirect(url_for('signup_login'))
    return render_template('buy_sell.html')

@app.route('/signup_login.html', methods=['GET', 'POST'])
def signup_login():
    return render_template('signup_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session.permanent = True  # making session permanent
    # Assume a successful login
    session['user'] = username  # Storing the username in the session
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    with open('static/users.txt', 'a') as file:
        file.write(f'{username},{email},{password}\n')

    session['user'] = username  # Storing the username in the session
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Removing the username from the session
    return redirect(url_for('index'))

@app.route('/view_products')
def view_products():
    # Fetch the products from the products.txt.
    products = []
    with open('static/products.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 2:  # ensuring there are exactly two parts
                product_name, product_description = parts
                products.append({'name': product_name, 'description': product_description})
            else:
                print(f"Unexpected line format in products.txt: {line.strip()}")
    
    return render_template('view_products.html', products=products)

@app.route('/submit_product', methods=['POST'])
def submit_product():
    if 'user' in session:  # checking if a user is logged in.
        product_name = request.form['productName']
        product_description = request.form['productDescription']

        with open('static/products.txt', 'a') as file:
            file.write(f'{product_name}|{product_description}\n')

        flash("Products submitted successfully. To see your products, View Available Products!")
        return redirect(url_for('buy_sell'))
    else:
        flash("To submit your products, Please log in!")
        return redirect(url_for('signup_login'))

if __name__ == '__main__':
    app.run(debug=True)