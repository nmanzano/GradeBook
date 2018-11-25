import sqlite3
import os.path
from datetime import datetime
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


def selective_query_db(query, args=(), one=False):
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
    return db


@app.template_filter()
def datetimeformat(value):
    datetime_object = datetime.strptime(value, '%Y-%m-%d').strftime('%m/%d/%Y')
    return datetime_object


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    all_students = (all_query_db('SELECT * from student'))
    return render_template('dashboard.html', all_students=all_students)


@app.route('/student_profile', methods=['GET', 'POST'])
def student_profile():
    content = {}
    print(request.args["student_id"], 'line 76')
    print(request.args["student_first"], 'line 77')
    print(request.args["student_last"], 'line 78')
    # print(request.args["student_first"], 'line 76')
    content['student_id'] = request.args['student_id']
    content['student_first'] = request.args['student_first'].upper()
    content['student_last'] = request.args['student_last'].upper()
    # liststudent = student.split()
    # print(liststudent[0], 'line 79')
    # print(liststudent[1], 'line 79')
    # print(liststudent[2], 'line 79')
    return render_template('student_profile.html', student=content)


@app.route('/student', methods=['GET', 'POST'])
def student():
    content = {}
    if request.method == "POST":
        user_input_first = request.form['first_name'].upper()
        user_input_last = request.form['last_name'].upper()
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
              selective_query_db("""
                              select username from admin where username = ?""",
                                 [user_input], one=True))
            if user:
                password = (selective_query_db(
                            'select password from admin where password = ?',
                            [password_input], one=True))
                if password:
                    return redirect('/dashboard')
                return redirect('/')
        except:
            return redirect('/')
    return redirect('/')


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
