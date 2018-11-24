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
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def select_query_db(query, args=(), one=False):
    db = get_db().execute(query, args)
    rv = db.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv


def all_query_db(query):
    db = get_db().execute(query)
    response = db.fetchall()
    return response


def post_db(query, args=(), one=False):
    db = get_db()
    db.cursor()
    db.execute(query, args)
    db.commit()
    db.close()
    return db


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # connectdb = sqlite3.connect(DATABASE)
    # crsr = connectdb.cursor()
    # all_users = 'SELECT * from student'
    # crsr.execute(all_users)
    # rows = crsr.fetchall()
    # connectdb.close()
    # print(rows, 'this is rows')
    return render_template('dashboard.html')


# def load_quiz():
#     connectdb = sqlite3.connect(DATABASE)
#     crsr = connectdb.cursor()
#     all_users = 'SELECT * from quiz'
#     crsr.execute(all_users)
#     rows = crsr.fetchall()
#     connectdb.close()
#     print(rows, 'this is rows')


@app.route('/student', methods=['GET', 'POST'])
def student():
    content = {}
    if request.method == "POST":
        user_input_first = request.form['first_name']
        user_input_last = request.form['last_name']
        if user_input_first and user_input_last:
            student_name = (post_db(
                    'INSERT INTO student(first_name, last_name) VALUES(?, ?)',
                    [user_input_first, user_input_last], one=True))
            content['student'] = user_input_first + ' ' + user_input_last
            content['success'] = True
        else:
            content['error'] = True
    return render_template('student.html', content=content)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == "POST":
        quiz_input = request.form['subject']
        number_input = request.form['num_of_questions']
        date_input = request.form['quiz_date']
        print(quiz_input, number_input, date_input)
        if quiz_input and number_input and date_input:
            student_name = (post_db(
                    """INSERT INTO quiz(
                    subject, num_of_questions, quiz_date
                    ) VALUES(?, ?, ?)""",
                    [quiz_input, number_input, date_input], one=True))
    all_quizzes = (all_query_db('SELECT * from quiz'))
    print(all_quizzes, 'this is line 115')
    return render_template('quiz.html', all_quizzes=all_quizzes)


@app.route('/user_auth', methods=['POST'])
def user_auth():
    if request.method == "POST":
        user_input = request.form['user']
        password_input = request.form['password']

        try:
            user = (
              select_query_db("""
                              select username from admin where username = ?""",
                              [user_input], one=True))
            if user:
                password = (select_query_db(
                            'select password from admin where password = ?',
                            [password_input], one=True))
                if password:
                    print(password, 'THIS IS PASSWORD!!')
                    return redirect('/dashboard')
                return redirect('/')
        except:
            return redirect('/')
    return redirect('/')


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
