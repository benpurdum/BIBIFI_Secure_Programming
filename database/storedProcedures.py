
import sqlite3
from werkzeug.security import generate_password_hash


def get_db_connection():
    db = sqlite3.connect('database/database.db')
    return db


def insertUser(username, password, role, name, age):
    db = get_db_connection()

    password = generate_password_hash(password)

    cursor = db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))

    userID = cursor.lastrowid

    db.execute("INSERT INTO persons (userID, name, age) VALUES (?, ?, ?)", (userID, name, age))

    db.commit()
    db.close()


def createEvent(time, date, room, name):
    db = get_db_connection()

    db.execute("INSERT INTO galleryEvents (time, date, room, name) VALUES (?, ?, ?, ?)", (time, date, room, name))

    db.commit()
    db.close()


def seeEventHistory():
    db = get_db_connection()

    events = db.execute("SELECT * FROM galleryEvents").fetchall()

    db.close()
    return events


def createRoom(name, numPeople, art):
    db = get_db_connection()

    db.execute("INSERT INTO rooms (name, numPeople, art) VALUES (?, ?, ?)", (name, numPeople, art))

    db.commit()
    db.close()


def changeRooms(userID, fromRoom, toRoom, time, date):
    db = get_db_connection()

    try:
        db.execute("BEGIN")

        db.execute("UPDATE rooms SET numPeople = numPeople - 1 WHERE name = ?", (fromRoom,))

        db.execute("UPDATE rooms SET numPeople = numPeople + 1 WHERE name = ?", (toRoom,))

        db.execute("UPDATE persons SET currentRoom = ? WHERE userID = ?", (toRoom, userID))

        db.execute("INSERT INTO auditLogs (userID, time, date, fromRoom, toRoom) VALUES (?, ?, ?, ?, ?)", (userID, time, date, fromRoom, toRoom))

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def viewAllRooms():
    db = get_db_connection()

    rooms = db.execute("SELECT * FROM rooms").fetchall()

    db.close()
    return rooms


def addSession(userID, loginTime, loginDate):
    db = get_db_connection()

    cursor = db.execute("INSERT INTO sessions (userID, loginTime, loginDate) VALUES (?, ?, ?)", (userID, loginTime, loginDate))

    sessionID = cursor.lastrowid

    db.commit()
    
    db.close()
    return sessionID

def endSession(sessionID, logoutTime, logoutDate):
    db = get_db_connection()

    db.execute("UPDATE sessions SET logoutTime = ?, logoutDate = ? WHERE sessionID = ?", (logoutTime, logoutDate, sessionID))

    db.commit()
    db.close()


def addAuditLog(userID, time, date, fromRoom, toRoom):
    db = get_db_connection()

    db.execute("INSERT INTO auditLogs (userID, time, date, fromRoom, toRoom) VALUES (?, ?, ?, ?, ?)", (userID, time, date, fromRoom, toRoom))

    db.commit()
    db.close()


def changeCurrentRoom(userID, newRoom):
    db = get_db_connection()

    person = db.execute("SELECT currentRoom FROM persons WHERE userID = ?", (userID,)).fetchone()

    if person is None:
        db.close()
        return

    oldRoom = person[0]

    if oldRoom != newRoom:
        if oldRoom is not None:
            db.execute("UPDATE rooms SET numPeople = numPeople - 1 WHERE name = ?", (oldRoom,))

        db.execute("UPDATE rooms SET numPeople = numPeople + 1 WHERE name = ?", (newRoom,))

        db.execute("UPDATE persons SET currentRoom = ? WHERE userID = ?", (newRoom, userID))

    db.commit()
    db.close()


def seeCurrentRoom(userID):
    db = get_db_connection()

    room = db.execute("SELECT currentRoom FROM persons WHERE userID = ?", (userID,)).fetchone()

    db.close()

    if room is None:
        return None

    return room[0]


def seeAuditHistory():
    db = get_db_connection()

    logs = db.execute("SELECT * FROM auditLogs").fetchall()

    db.close()
    return logs

def viewAllUsers():
    db = get_db_connection()

    users = db.execute("SELECT userID, username, role FROM users").fetchall()

    db.close()
    return users