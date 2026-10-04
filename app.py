from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from database.storedProcedures import (
    insertUser,
    createEvent,
    seeEventHistory,
    createRoom,
    changeRooms,
    viewAllRooms,
    addSession,
    endSession,
    seeAuditHistory,
    viewAllUsers
)

def get_db_connection():
    db = sqlite3.connect('database/database.db')
    return db

app = Flask(__name__)
app.secret_key = 'secureProgrammingKey'

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        account = cursor.fetchone()
        cursor.close()
        db.close()

        if account and check_password_hash(account[2], password):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['role'] = account[3]

            now = datetime.now()
            session['sessionID'] = addSession(
                account[0],
                now.strftime('%H:%M:%S'),
                now.strftime('%Y-%m-%d')
            )

            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password'

    return render_template('login.html', msg=msg)


# Home
@app.route('/home')
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    rooms = viewAllRooms()

    return render_template(
        'home.html',
        username=session['username'],
        role=session['role'],
        rooms=rooms
    )

# Log History
@app.route('/log')
def log():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] not in ['Employee', 'Admin']:
        return redirect(url_for('home'))
    
    logs = seeAuditHistory()

    return render_template('log.html', logs=logs)

@app.route('/move_room', methods=['POST'])
def move_room():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    userID = session['id']
    newRoom = request.form['room']

    db = get_db_connection()
    person = db.execute("SELECT currentRoom FROM persons WHERE userID = ?", (userID,)).fetchone()
    db.close()

    if person is None:
        return redirect(url_for('home'))

    oldRoom = person[0]

    if oldRoom != newRoom:
        now = datetime.now()
        changeRooms(userID, oldRoom, newRoom, now.strftime('%H:%M:%S'), now.strftime('%Y-%m-%d'))

    return redirect(url_for('home'))

# User Management
@app.route('/users')
def manage_users():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] != 'Admin':
        return redirect(url_for('home'))

    users = viewAllUsers()

    return render_template('users.html', users=users)


# Create User
@app.route('/create_user', methods=['POST'])
def create_user():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] != 'Admin':
        return redirect(url_for('home'))

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    name = request.form['name']
    age = request.form['age']

    if role not in ['Guest', 'Employee', 'Admin']:
        return redirect(url_for('manage_users'))

    insertUser(username, password, role, name, age)

    return redirect(url_for('manage_users'))


# Record Gallery Event
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] not in ['Employee', 'Admin']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']

        now = datetime.now()
        createEvent(now.strftime('%H:%M:%S'), now.strftime('%Y-%m-%d'), room, name)

        return redirect(url_for('event_history'))

    rooms = viewAllRooms()

    return render_template('create_event.html', rooms=rooms)


# Event History
@app.route('/event_history')
def event_history():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    events = seeEventHistory()

    return render_template('event_history.html', events=events)

# Create Room
@app.route('/create_room', methods=['POST'])
def create_room():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] != 'Admin':
        return redirect(url_for('home'))

    name = request.form['name']
    numPeople = request.form['numPeople']
    art = request.form['art']

    createRoom(name, numPeople, art)

    return redirect(url_for('home'))

# Logout
@app.route('/login/logout')
def logout():
    if 'loggedin' in session and 'sessionID' in session:
        now = datetime.now()
        endSession(session['sessionID'], now.strftime('%H:%M:%S'), now.strftime('%Y-%m-%d'))

    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)