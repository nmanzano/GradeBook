import sqlite3
import click
import os.path

from flask import Flask
from flask import current_app, g
from flask.cli import with_appcontext

app = Flask(__name__)


def create_db():
    if os.path.exists('hw12.db'):
        try:
            conn = sqlite3.connect('hw12.db')
            print(sqlite3.version, 'VERSION')
        except Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print('not here')
        import db
        db.init_db()
        create_db()


@app.route('/')
def hello_world():
    return 'Hello Cheese'


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
