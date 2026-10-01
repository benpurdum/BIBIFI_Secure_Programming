from flask import Flask, render_template, request, redirect, url_for, session
import config
from werkzeug.security import check_password_hash

db = _______
app = Flask(__name__)


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

        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s",(username))
        account = cursor.fetchone()
        cursor.close()

        if account and check_password_hash(account[2], password):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['role'] = account[3]
            return redirect(url_for('home'))

        msg = 'Incorrect username or password'

    return render_template('login.html', msg=msg)


# Home
@app.route('/home')
def home():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    return render_template(
        'home.html',
        username=session['username'],
        role=session['role']
    )

# Logout
@app.route('/login/logout')
def logout():
    session.pop('loggedin')
    session.pop('id')
    session.pop('username')
    session.pop('role')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)