from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from storedProcedures import (
    insertUser,
    createEvent,
    seeEventHistory,
    createRoom,
    changeRooms,
    viewAllRooms,
    addSession,
    endSession,
    seeAuditHistory,
    viewAllUsers,
    seeCurrentRoom,
    getSessions,
    getRoomNames
)

DATABASE_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "database.db"
)

def get_db_connection():
    db = sqlite3.connect(DATABASE_PATH)
    return db

app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")
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
            session.clear()

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
    cRoom = seeCurrentRoom(session['id'])

    image = ""
    alt = ""
    match cRoom:
        case "Gallery":
            image = "images/bigTree.jpg"
            alt = "A Large, Red Tree"
        case "Room 1":
            image = "images/droopyPurpleFlowers.jpg"
            alt = "Droopy, Purple Flowers"
        case "Room 2":
            image = "images/redFlowers.jpg"
            alt = "Red Flowers"
        case "Room 3":
            image = "images/whiteFlowers.jpg"
            alt = "White Flowers"
        case "Lobby":
            image = "images/purpleFlowers.jpg"
            alt = "Purple Flowers"

    return render_template(
        'home.html',
        username=session['username'],
        role=session['role'],
        rooms=rooms,
        cRoom=cRoom,
        image = image,
        alt = alt
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

# Session History
@app.route('/audit_log')
def audit_log():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if session['role'] != 'Admin':
        return redirect(url_for('home'))
    
    alogs = getSessions()

    return render_template('audit_log.html', logs=alogs)

@app.route('/move_room', methods=['POST'])
def move_room():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    userID = session['id']
    newRoom = request.form['room']
    rooms = getRoomNames()
    for i in range(0,len(rooms)):
         rooms[i] = rooms[i][0]
    if newRoom not in rooms:
        return render_template('error.html', msg="Invalid room")

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

    uid = request.form['id']
    if not uid.isdigit():
         return render_template('error.html', msg="Invalid user ID")
    username = request.form['username']
    if len(username)>20:
            return render_template('error.html', msg="Username too long")
    password = request.form['password']
    role = request.form['role']
    name = request.form['name']
    if len(name)>30:
        return render_template('error.html', msg="Name too long")
    age = request.form['age']
    if not age.isdigit():
        return render_template('error.html', msg="Invalid age")

    if role not in ['Guest', 'Employee', 'Admin']:
        return render_template('error.html', msg="Invalid role")

    insertUser(uid, username, password, role, name, age)

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
        if len(name)>30:
                        return render_template('error.html', msg="Name too long")
        rooms = getRoomNames()
        for i in range(0,len(rooms)):
            rooms[i] = rooms[i][0]
        if room not in rooms:
                return render_template('error.html', msg="Invalid room")

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
    if len(name)>30:
        return render_template('error.html', msg="Name too long")
    numPeople = "0"
    art = request.form['art']
    if len(name)>30:
        return render_template('error.html', msg="Art name too long")

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
    app.run()