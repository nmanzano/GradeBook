import sqlite3


def init_db():
    conn = sqlite3.connect('hw12.db')
    crsr = conn.cursor()
    fd = open('schema.sql', 'r')
    sqlFile = fd.read()
    crsr.executescript(sqlFile)

    crsr.execute("INSERT INTO admin(username, password) VALUES(?, ?)", ('admin', 'password'))
    conn.commit()

    crsr.execute("select * from admin")
    rows = crsr.fetchall()
    conn.close()
    fd.close()
    print(rows, 'this is rows')
