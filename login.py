# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = '1'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '80.212.175.9'
app.config['MYSQL_USER'] = 'Hesterbest'
app.config['MYSQL_PASSWORD'] = 'Scrummedaddy!!'
app.config['MYSQL_DB'] = 'ga_bibliotek'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        # hash = password + app.secret_key
        # hash = hashlib.sha1(hash.encode())
        # password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM låner WHERE Epost = %s AND Passord = %s', (username, password,))
        # Fetch one record and return the result
        låner = cursor.fetchone()
        # If account exists in accounts table in out database
        if låner:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = låner['LNr']
            session['username'] = låner['Epost']
            if låner['isAdmin'] == 1:
                session['isAdmin'] = True
                return 'You are an admin!'
            else:
                session['isAdmin'] = False
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('isAdmin', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register
# - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        address = request.form['address']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM låner WHERE Epost = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+(?:,?\s*)*', address):
            msg = 'Address must contain only characters, spaces, commas and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Name must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', surname):
            msg = 'Surname must contain only characters and numbers!'

        elif not username or not password or not name or not surname or not address:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            # hash = password + app.secret_key
            # hash = hashlib.sha1(hash.encode())
            # password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('''INSERT INTO låner VALUES 
                            (0, %s, %s, %s, %s, 0, %s)''',
                           (name, surname, address, username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
