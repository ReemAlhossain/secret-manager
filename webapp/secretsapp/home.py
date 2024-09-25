
from flask import Blueprint, render_template, request, session , redirect, url_for
from flask import g as app_context_global
from.db import db_connection
import mysql.connector   # Importing the MySQL connector library
import json
from datetime import datetime, timedelta

from passlib.hash import argon2

from argon2 import PasswordHasher
from flask import flash




bp = Blueprint("bp", __name__)

def db_connection():
    """This function can be called to access the database connection while handling a request"""
    if 'db' not in app_context_global:
        # TODO: store config in config file
        # TODO: do not store secrets on git

        app_context_global.db = mysql.connector.connect(
            host="localhost",
            port="5360",
            user="secrets",
            password="BestPassword",
            database="secrets",
        )
    return app_context_global.db

@bp.route("/")
def index():
    return render_template("home/index.html")


@bp.route('/Auth', methods=['GET', 'POST'])
def Auth():
    # Check if the request method is POST and if 'username' and 'password' are present in the form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Establish a connection to the database
        db = db_connection()
        cursor = db.cursor(dictionary=True)  # Create a cursor for executing queries

        # Check if the account exists in the database
        cursor.execute('SELECT password_hash FROM User WHERE username = %s', (username,))
        result = cursor.fetchone()

        if result is not None:
            stored_hash = result['password_hash']

        # Check if the password matches the stored hash
        is_verified = argon2.verify(password, stored_hash)

        if is_verified:
            # Handle successful login
            session['loggedin'] = True
            session['username'] = username

            # Add 'just_logged_in' to the session to keep track of recent login
            session['just_logged_in'] = True
            return redirect(url_for('bp.my_secrets'))
        else:
            # If no matching account is found, render the 'Contact.html' template
            return render_template('home/Contact.html')

    # Render the 'index.html' template if the conditions are not met
    return render_template('home/index.html')



@bp.route('/MySecrets')
def my_secrets():
    if 'loggedin' in session:
        username = session['username']
 
        # Establish a connection to the database
        db = db_connection()
        cursor = db.cursor(dictionary=True)
 
        # Fetch secrets for the user
        cursor.execute("SELECT geheimen FROM Secret WHERE user_name = %s LIMIT 0, 10", (username,))
        all_secrets = cursor.fetchall()
 
        # Initialize login_data as an empty list
        login_data = []
 
        # Check if last_login is already stored in the session
        if 'last_login' in session:
            last_login = session['last_login']
        else:
            # If last_login hasn't been retrieved yet, fetch it from the database
            cursor.execute('SELECT last_login FROM User WHERE username = %s', (username,))
            row = cursor.fetchone()
            if row and row['last_login'] is not None:
                login_data = json.loads(row['last_login'])
                if login_data:
                    last_login = max(login_data)
                else:
                    last_login = []
            else:
                last_login = []
 
            # Store last_login in the session to avoid fetching it again
            session['last_login'] = last_login
 
        # Convert login_data to a list before appending the timestamp
        login_data = list(login_data)
 
        # Add the current login time only if the user has just logged in
        if 'just_logged_in' in session:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            login_data.append(timestamp)
 
            # Update the login data in the database
            cursor.execute('UPDATE User SET last_login = %s WHERE username = %s',
                           (json.dumps(login_data), username))
            db.commit()
 
        # Close the database connection
        db.close()
 
        return render_template('home/MySecrets.html', username=username, all_secrets=all_secrets, last_login=last_login)
    else:
        return render_template('home/index.html')



    


@bp.route('/edit_secret', methods=['POST'])
def edit_secret():
    # Get the values from the form
    geheimen_value = request.form.get('secret_id')
    new_value = request.form.get('new_value')
    login_data = session['last_login']  # Get the login data from the session
    username = session['username']  # Get the username from the session
 
    # Perform the edit operation (e.g., fetch and update from the database)
    db = db_connection()  # Establish a database connection
    cursor = db.cursor(dictionary=True)  # Create a cursor for executing queries
 
    # Update the 'geheimen' value in the database
    cursor.execute("UPDATE Secret SET geheimen = %s WHERE geheimen = %s", (new_value, geheimen_value))
    db.commit()  # Commit the changes to the database
 
    # Refetch the updated data from the database
    cursor.execute("SELECT geheimen FROM Secret WHERE user_name = %s LIMIT 0, 10", (username,))
    all_secrets = cursor.fetchall()
 
    db.close()  # Close the database connection
 
    # Redirect back to MySecrets after editing
    return render_template('home/MySecrets.html', username=username, all_secrets=all_secrets, last_login=login_data)



@bp.route('/delete_secret', methods=['POST'])
def delete_secret():
    # Get the value of 'secret_id' from the form
    geheimen_value = request.form.get('secret_id')
    
    # Get the 'last_login' data from the session
    login_data = session['last_login']
    
    # Establish a connection to the database
    db = db_connection()
    cursor = db.cursor(dictionary=True)
 
    # Delete the secret with the specified value from the database
    cursor.execute("DELETE FROM Secret WHERE geheimen = %s", (geheimen_value,))
    db.commit()
 
    # Fetch the updated data after deletion
    username = session['username']
    cursor.execute("SELECT geheimen FROM Secret WHERE user_name = %s LIMIT 0, 10", (username,))
    all_secrets = cursor.fetchall()
 
    # Render the 'MySecrets.html' template with updated data
    return render_template('home/MySecrets.html', username=username, all_secrets=all_secrets, last_login=login_data)


@bp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None) # Remove the 'loggedin' key from the session (if it exists)
   session.pop('username', None) # Remove the 'username' key from the session (if it exists)
   session.pop('last_login', None) # Remove the 'last_login' key from the session (if it exists)
   # After removing session data, redirect to the index page
   return render_template('home/index.html')


@bp.route('/registration',methods=['GET', 'POST'])
def reg():
    # Check if the request method is POST and if 'username', 'password', and 'email' are in the form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Get the values from the form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Establish a database connection
        db = db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Check if the username already exists
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
            return render_template('home/Registration.html', msg=msg)
        else:
            # If username is new, insert into the database
            db = db_connection()
            cursor = db.cursor(dictionary=True) # Create a cursor for executing queries
            hasher = PasswordHasher()

            hashed_password = argon2.using(rounds=4).hash(password)
            cursor.execute("INSERT INTO secrets.User (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
            db.commit()   # Commit the changes to the database
            msg = 'You have successfully registered!'
            return render_template('home/Registration.html', msg=msg)
            
    # If the request method is not POST or form fields are missing, go to the index page
    return render_template('home/index.html')




    
@bp.route('/manage_password', methods=['POST'])
def manage_password():
    username = session['username']
    password_input = request.form['password']
    login_data = session['last_login']

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) FROM Secret WHERE user_name = %s", (username,))
    num_rows = cursor.fetchone()['COUNT(*)']
    cursor.execute("SELECT geheimen FROM Secret WHERE user_name = %s LIMIT 0, 10", (username,))
    all_secrets = cursor.fetchall()

    if num_rows >= 10:
        msg = "Sorry, you've reached the maximum limit of secrets (10)."
        flash(msg, 'error')  # Flash an error message
        return render_template('home/MySecrets.html', username=username, all_secrets=all_secrets, msg=msg)
    else:
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO Secret (user_name, geheimen) VALUES (%s, %s)", (username, password_input))
        cursor.execute("SELECT geheimen FROM Secret WHERE user_name = %s LIMIT 0, 10", (username,))
        all_secrets = cursor.fetchall()
        db.commit()
        db.close()
        msg = 'Your secret added successfully !'
        flash(msg, 'success')  # Flash a success message
        #return redirect(url_for('bp.my_secrets'))  # Redirect to 'my_secrets' after adding the secret
        return render_template('home/MySecrets.html', username=username, all_secrets=all_secrets,msg=msg, last_login=login_data)















