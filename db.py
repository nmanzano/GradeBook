import sqlite3


def init_db():
    conn = sqlite3.connect('hw12.db')
    crsr = conn.cursor()
    fd = open('schema.sql', 'r')
    sqlFile = fd.read()
    crsr.executescript(sqlFile)
    conn.close()
    fd.close()
