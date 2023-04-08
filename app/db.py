import sqlite3, random, datetime
from models import User


def getNewId():
    return random.getrandbits(28)


users = [    
    {
        'active': True,
        'username': 'nci_naseem_1',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_2',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_3',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': "nci_naseem_4",
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_5',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_6',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_7',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_8',
        'timestamp': datetime.datetime.now()
    },
    {
        'active': True,
        'username': 'nci_naseem_9',
        'timestamp': datetime.datetime.now()
    },
]    

def connect():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, active BOOLEAN, username TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in users:
        user = User(getNewId(), i['active'], i['username'], i['timestamp'])
        insert(user)

def insert(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?,?)", (
        user.id,
        user.active,
        user.username,
        user.timestamp
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    users = []
    for i in rows:
        user = User(i[0], True if i[1] == 1 else False, i[2], i[3])
        users.append(user)
    conn.close()
    return users

def update(user):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET active=?, username=? WHERE id=?", (user.active, user.username, user.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()