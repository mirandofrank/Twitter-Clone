<<<<<<< HEAD
# Frank Mirando, mirandofrank@csu.fullerton.edu
# Ivan Parrales, iparrales@csu.fullerton.edu
# Mina Moslehpour, mmoslehpour@csu.fullerton.edu
=======
#CPSC 449 Project 2 by Ivan Parrales, Frank Mirando, and Mina Moslehpour

>>>>>>> 930d97aa8385a41041d7baa077748ff59d6d0a96
import flask
from flask import request, jsonify, g, current_app
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)

#Function to help return json fomrat  
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#Following functions create the custom command for flask init that runs the schema and creates database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory
    return g.db


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_db(e=None):
    if e is not None:
        print(f'Closing db: {e}')
    db = g.pop('db', None)
    if db is not None:
        db.close()


#This can be commented out. Not really needed for the project
@app.route('/', methods=['GET'])
def gome():
    return "<h1>Microservice for Users</h1><p>This is the microservice for the users</p>"


#Return all available users in the database
@app.route('/users/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM USERS;').fetchall()

    return jsonify(all_users), 201


#Registers a new user to the database
@app.route('/register', methods=['POST'])
def createUser():
    userInfo = request.get_json()
    username = userInfo.get('username')
    email = userInfo.get('email')
    password = userInfo.get('password')
    hashed_password = generate_password_hash(password)
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO USERS VALUES(?,?,?)', (username, email, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(message=username + ' was registered successfully.'), 201 


#Logs in a user by comparing the username and password given with the username and password in the database 
@app.route('/login', methods=['POST'])
def authenticateUser():
    userInfo = request.get_json()
    username = userInfo.get('username')
    password = userInfo.get('password')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userPassword = cur.execute('SELECT PASSWORD FROM USERS WHERE USERNAME = ?', [username]).fetchone()[0]
    
    if check_password_hash(userPassword, password):
        return jsonify(message=username + ' was authenticated successfully.'), 201 
    else:
        return jsonify(message=username + ' password incorrect' ), 401 


#Adds a new follower to the username given
@app.route('/follow', methods=['PUT'])
def addFollower():
    userInfo = request.get_json()
    username = userInfo.get('username')
    usernameToFollow = userInfo.get('usernameToFollow')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO FOLLOWERS (FOLLOWING, USER) VALUES(?,?)',(usernameToFollow, username))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(message=username + ' is now following ' + usernameToFollow), 200


#Stop following a user.
@app.route('/unfollow', methods=['POST'])
def removeFollower():
    userInfo = request.get_json()
    username = userInfo.get('username')
    usernameToRemove = userInfo.get('usernameToRemove')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM FOLLOWERS WHERE USER = ? AND FOLLOWING = ?',(username, usernameToRemove))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify(message=username + ' is now unfollowing ' + usernameToRemove),200



#Error checking
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404</h1>
    <p>The resource could not be found.</p>''', 404


if __name__ == '__main__':
    app.run()
