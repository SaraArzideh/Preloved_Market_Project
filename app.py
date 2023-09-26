# pip install -r requierments.txt


from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key='your_secret_key' # set a secret key for session management

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
    
    # Handling signup and login.
    if request.method == 'POST':
        # Handling signup/login
        pass
    return render_template('signup_login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    # Assume a successful login
    session['user'] = username  # Store the username in the session
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    # Assume a successful login
    session['user'] = username  # Store the username in the session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)