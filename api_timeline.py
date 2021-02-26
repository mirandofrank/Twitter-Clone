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
import time, datetime

DATABASE = 'database.db'
DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)

#Similar to api_users just to help return in json format 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#Similar to api_users, functuions to make it so flask init
#creates the database from the schema file
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


#Can also be commented out. Not needed for final project
@app.route('/', methods=['GET'])
def gome():
    return "<h1>Microservice for Users</h1><p>This is the microservice for the users</p>"


#Returns recent tweets from a user.
@app.route('/userTimeline', methods=['GET'])
def getUserTimeline():
    userInfo = request.get_json()
    username = userInfo.get('username')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userTimeline = cur.execute('SELECT * FROM TWEETS WHERE AUTHOR = ? LIMIT 25', (username)).fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(userTimeline), 201 


#Returns 25 tweets from all users
@app.route('/publicTimeline', methods=['GET'])
def getPublicTimeline():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    recentTweets = cur.execute('SELECT * FROM TWEETS ORDER BY TIME_STAMP DESC LIMIT 25;').fetchall()

    return jsonify(recentTweets), 201


#Post a new tweet.
@app.route('/postTweet', methods=['POST'])
def postTweet():
    postTime = time.time()
    date = str(datetime.datetime.fromtimestamp(postTime).strftime('%Y-%m-%d %H:%M:%S'))

    tweetInfo = request.get_json()
    username = tweetInfo.get('username')
    tweetText = tweetInfo.get('tweet')
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO TWEETS (TWEET, TIME_STAMP, AUTHOR) VALUES(?,?,?)', (tweetText, date, username))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(message= username + ' posted: ' + tweetText), 201


#Home Timeline aka the most recent tweets from your followers
@app.route('/homeTimeline', methods=['GET'])
def getHomeTimeline():
    userInfo = request.get_json()
    username = userInfo.get('username')
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    homeTweets = cur.execute('SELECT TWEET,TIME_STAMP,AUTHOR FROM TWEETS INNER JOIN FOLLOWERS ON FOLLOWERS.FOLLOWING = TWEETS.AUTHOR WHERE FOLLOWERS.USER =? ORDER BY TIME_STAMP DESC LIMIT 25',(username)).fetchall()
    return jsonify(homeTweets), 201


#Error checking
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404</h1>
    <p>The resource could not be found.</p>''', 404


if __name__ == '__main__':
    app.run()
 
