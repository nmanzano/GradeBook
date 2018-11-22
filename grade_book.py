import sqlite3
import os.path

from flask import Flask, render_template, g, redirect, request

app = Flask(__name__)

DATABASE = 'hw12.db'


def create_db():
    if os.path.exists(DATABASE):
        print('Connecting to Database...')
        try:
            conn = sqlite3.connect(DATABASE)
            print('Connected to Database')
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print('Creating Database...')
        import db
        db.init_db()
        create_db()


def get_db():
    print('made it to get_db?')
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    print(db, 'this is db')
    return db


def query_db(query, args=(), one=False):
    print('made it to query_db?')
    cur = get_db().execute(query, args)
    print('line 40')
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/user_auth', methods=['POST'])
def user_auth():
    if request.method == "POST":
        user_input = request.form['user']
        password_input = request.form['password']

        try:
            user = query_db('select username from admin where username = ?', [user_input], one=True)
            if user:
                password = query_db('select password from admin where password = ?', [password_input], one=True)
                if password:
                    print(password, 'THIS IS PASSWORD!!')
                    return redirect('/dashboard')
                return redirect('/')
        except:
            print('THIS IS EXCEPT!')
            return redirect('/')
    return redirect('/')


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
