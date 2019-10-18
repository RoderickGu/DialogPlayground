# Import the Flask package
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# Define the index route
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    print("*"*10)
    json['response'] = "this is a response"
    socketio.emit('my response', json, callback=messageReceived)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=True, nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
#    date_posted = db.Column(db.DataTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


@app.route('/session')
def sessions():
    return render_template('sessions.html', sysoutput="kidding")

# Run Flask if the __name__ variable is equal to __main__
if __name__ == "__main__":
    #app.run()
    socketio.run(app, debug=True)
